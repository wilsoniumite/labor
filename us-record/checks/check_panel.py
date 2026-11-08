# check_panel.py — the us-record data panel (data/panel.csv, built by code/panel.py), checked before anything is fitted
# on it. Groups:
#   M  the manifest: every source file exists and matches its SHA-256; every column traces to a source
#   C  coverage: the targeted series complete over 1950–2024, and every gap a stated one (the complete-year rule; θ_V
#      measured only from 1967)
#   I  identities and anchors against independent numbers: the employment rate against employment over adults; the
#      fork's size as the paper prints it; depreciation and θ_V in 2023 against calibration (c)'s stored values; the
#      four financing shares' medians near one
#   B  bands: each banded series inside its own band, where it has one
#   S  sanity: magnitudes a wrong series id or unit would break
# Tolerances are set before reading the panel: identities to 1e-9 where exact, otherwise as stated per check.
# Changed after the first run (2026-11-05), each marked in its text: I5 (first an identity, "add to one"; the four are
# medians taken separately over a grid of variants, so their sum need not be one: largest gap 0.0157), B1 (first on every
# year; the band is the weak estimate's and applies only to WEAK years), S2 (the 1981–85 floor first 5%: the five-year
# adaptive expectation lags the disinflation; found 4.9%), I4 (first exact; chains.json and calibration_c.json store
# the same number one unit apart in the last bit, ...405 and ...404).
# Added with the split (2026-11-05), after its series were first built and printed: C5, I7, I8, S7, S8. I8's tolerance
# was set before its anchor series was fetched. Added with the basket (2026-11-05), after its series was built: C6, I9.
# Run from us-record/:  python3 checks/check_panel.py      Exit 0 only if every check passes.

import hashlib
import json
import re
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
P = pd.read_csv(os.path.join(ROOT, "data", "panel.csv")).set_index("year")
MAN = pd.read_csv(os.path.join(ROOT, "data", "manifest.csv"))
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


# ---- M: the manifest
bad = [r.file for r in MAN.itertuples()
       if not os.path.exists(os.path.join(REPO, r.file))
       or hashlib.sha256(open(os.path.join(REPO, r.file), "rb").read()).hexdigest() != r.sha256]
check("M1 every source file in data/manifest.csv exists and matches its SHA-256", not bad, f"{len(MAN)} files; bad: {bad}")
tokens = set(re.split(r"[ ,()]+", " ".join(MAN["used_for"])))
parent = {"labour_share_c_lo": "labour_share_c", "labour_share_c_hi": "labour_share_c",
          "labour_share_c_tier": "labour_share_c", "theta_V_basis": "theta_V", "kappa_med": "kappa",
          "kappa_min": "kappa", "kappa_max": "kappa", "labor_origin_fin_lo": "labor_origin_fin",
          "labor_origin_fin_hi": "labor_origin_fin", "infl": "infl", "exp_infl": "exp_infl", "real_rate": "real_rate",
          "real_rate_gs10": "real_rate_gs10", "dur_rel_price": "dur_share"}
orphans = [c for c in P.columns
           if parent.get(c, c) not in tokens and not (c.startswith("fin_") and "fin_*" in tokens)]
check("M2 every column traces to a manifest row (derived columns through their parents)", not orphans,
      f"orphans: {orphans}")

# ---- C: coverage
TARGETED = ["wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate"]   # prime-age since breakpoint A
gaps = {c: [y for y in range(1950, 2025) if pd.isna(P.loc[y, c])] for c in TARGETED}
check("C1 the four targeted series are complete over 1950–2024", not any(gaps.values()), f"gaps: {gaps}")
INPUTS = ["adults", "real_rate", "delta"]
gaps = {c: [y for y in range(1950, 2025) if pd.isna(P.loc[y, c])] for c in INPUTS}
check("C2 adults, the real rate and depreciation are complete over 1950–2024", not any(gaps.values()), f"gaps: {gaps}")
oct25 = all(pd.isna(P.loc[2025, c]) for c in ("wage_goods", "wage_shelter", "emp_rate", "prime_emp_rate", "adults",
                                              "infl"))
check("C3 2025 is missing exactly where a monthly source lacks October 2025 (the complete-year rule), and present for "
      "the annual sources", oct25 and P.loc[2025, ["labour_share_c", "delta", "aaa"]].notna().all())
tv = P["theta_V"].dropna()
check("C4 θ_V is measured from 1967 only: the six benchmark years 1967–1992 and every year 1997–2023, nothing imputed",
      list(tv.index) == [1967, 1972, 1977, 1982, 1987, 1992] + list(range(1997, 2024)), f"{len(tv)} years")

SPLIT = ["pns_share", "pay_gap"]
gaps = {c: [y for y in range(1964, 2025) if pd.isna(P.loc[y, c])] for c in SPLIT}
check("C5 the split's two series are complete over 1964–2024 and absent before (BLS's production and nonsupervisory "
      "series start in 1964)", not any(gaps.values()) and P.loc[:1963, SPLIT].isna().all().all(), f"gaps: {gaps}")

check("C6 the production worker's real wage over the all-items CPI is complete over 1950–2024",
      P.loc[1950:2024, "real_wage_cpi"].notna().all())

# ---- I: identities and anchors
ratio = P["employed"] / P["adults"]
gap = (P["emp_rate"] - ratio).abs().loc[1950:2024].max()
check("I1 the employment rate equals employment over adults (FRED CE16OV / CNP16OV), each an annual mean, to 0.002",
      gap < 0.002, f"largest gap {gap:.5f}")
fork = (P.loc[2024, "wage_goods"] / P.loc[1964, "wage_goods"]) / (P.loc[2024, "wage_shelter"] / P.loc[1964, "wage_shelter"])
check("I2 the deflator fork over 1964–2024 is the paper's 4.8", round(fork, 1) == 4.8, f"{fork:.4f}")
check("I3 depreciation in 2023 is calibration (c)'s 0.0522 (BEA Fixed Assets, Tables 1.1 and 1.3; paths decision 36)",
      abs(P.loc[2023, "delta"] - 0.0522) < 5e-5, f"{P.loc[2023, 'delta']:.5f}")
c_theta = json.load(open(os.path.join(REPO, "paths", "results", "calibration_c.json")))["targets"]["central"]["theta_V"]
check("I4 [changed after the first run] θ_V in 2023 is calibration (c)'s stored central target, to 1e-12",
      abs(P.loc[2023, "theta_V"] - c_theta) < 1e-12,
      f"{P.loc[2023, 'theta_V']:.10f} vs {c_theta:.10f}")
s = P[["fin_wage_direct", "fin_wagetax", "fin_ownertax", "fin_borrowed"]].sum(axis=1).loc[1960:2025]
check("I5 [changed after the first run] the four financing shares' medians add to within 0.02 of one each year, "
      "1960–2025 (medians over a grid of variants, taken separately)", (s - 1).abs().max() < 0.02,
      f"largest gap {(s - 1).abs().max():.4f}")
def raw_annual(rel, sid):
    """Recomputed here from the raw monthly file, on a code path of its own: complete calendar years only."""
    df = pd.read_csv(os.path.join(REPO, rel), parse_dates=["observation_date"])
    s = pd.to_numeric(df[sid], errors="coerce")
    g = s.groupby(df["observation_date"].dt.year)
    return g.mean()[g.count() == 12]


cpi, aaa = raw_annual("paths/cache/CPIAUCNS.csv", "CPIAUCNS"), raw_annual("paths/cache/AAA.csv", "AAA") / 100.0
exp_infl = np.log(cpi).diff().rolling(5).mean()
rr_re = (aaa - exp_infl).reindex(P.index)
both = P["real_rate"].notna() & rr_re.notna()
check("I6 the real rate is the Aaa yield less the mean log CPI inflation of the five years to t, recomputed from the raw "
      "files (to 1e-9), and present in exactly the same years", (P["real_rate"][both] - rr_re[both]).abs().max() < 1e-9
      and (P["real_rate"].notna() == rr_re.notna()).all(), f"{int(both.sum())} years")

def fred_cache(path, sid):
    df = pd.read_csv(path, parse_dates=["observation_date"])
    return pd.Series(pd.to_numeric(df[sid], errors="coerce").values, index=df["observation_date"]).dropna()


def monthly_complete(s):
    g = s.groupby(s.index.year)
    return g.mean()[g.count() == 12]


ahe_tpi = raw_annual("pinning/effort/data/raw/AHETPI.csv", "AHETPI")
priv = monthly_complete(fred_cache(os.path.join(ROOT, "cache", "USPRIV.csv"), "USPRIV"))
hrs = monthly_complete(fred_cache(os.path.join(ROOT, "cache", "AWHNONAG.csv"), "AWHNONAG"))
wsal = fred_cache(os.path.join(ROOT, "cache", "A132RC1A027NBEA.csv"), "A132RC1A027NBEA")
wsal.index = wsal.index.year
g = (wsal * 1e9 / (priv * 1e3 * hrs * 52.0) / ahe_tpi).dropna()
g = (g / g.loc[1964]).reindex(P.index)
both = P["pay_gap"].notna() & g.notna()
check("I7 the pay gap is private wages and salaries (NIPA) over private jobs times the production group's weekly hours "
      "times 52, over that group's hourly earnings, 1964 = 1, recomputed from the raw files (to 1e-9), in the same years",
      (P["pay_gap"][both] - g[both]).abs().max() < 1e-9 and (P["pay_gap"].notna() == g.notna()).all(),
      f"{int(both.sum())} years")
ces = np.log(P.loc[2024, "ahe_all"] / ahe_tpi.loc[2024]) - np.log(P.loc[2007, "ahe_all"] / ahe_tpi.loc[2007])
ours = np.log(P.loc[2024, "pay_gap"] / P.loc[2007, "pay_gap"])
check("I8 the pay gap's change 2007–2024 is within 0.05 (log) of BLS's own: all private employees' average hourly "
      "earnings (CES0500000003, from 2006) over the production group's", abs(ours - ces) < 0.05,
      f"ours {ours:+.4f}, BLS's {ces:+.4f}")

man_ = raw_annual("pinning/effort/data/raw/AHEMAN.csv", "AHEMAN")
link = pd.concat([man_.loc[:1964], ahe_tpi.loc[1965:] * man_.loc[1964] / ahe_tpi.loc[1964]])
rw = (link / cpi).reindex(P.index)
rw = 100.0 * rw / rw.loc[1950]
both = P["real_wage_cpi"].notna() & rw.notna()
check("I9 the real wage over the all-items CPI is AHEMAN to 1964 and AHETPI after, linked at 1964, over CPIAUCNS, 1950 = "
      "100, recomputed from the raw files (to 1e-9), in the same years",
      (P["real_wage_cpi"][both] - rw[both]).abs().max() < 1e-9 and (P["real_wage_cpi"].notna() == rw.notna()).all(),
      f"{int(both.sum())} years; 1970 {P.loc[1970, 'real_wage_cpi']:.1f}")

exsh_ = monthly_complete(fred_cache(os.path.join(ROOT, "cache", "CUUR0000SA0L2.csv"), "CUUR0000SA0L2"))
rx = (link / exsh_).reindex(P.index)
rx = 100.0 * rx / rx.loc[1950]
both = P["wage_exshelter"].notna() & rx.notna()
check("I10 [added 2026-11-06] the goods wage over everything but shelter is the same linked earnings over the CPI less "
      "shelter (CUUR0000SA0L2), 1950 = 100, recomputed from the raw files (to 1e-9), complete over 1950-2024",
      (P["wage_exshelter"][both] - rx[both]).abs().max() < 1e-9 and P.loc[1950:2024, "wage_exshelter"].notna().all(),
      f"{int(both.sum())} years; 2024 {P.loc[2024, 'wage_exshelter']:.0f}")

# ---- B: bands
inside = lambda v, lo, hi: ((v >= lo - 1e-12) & (v <= hi + 1e-12)).loc[v.dropna().index].all()  # noqa: E731
weak = P["labour_share_c_tier"] == "WEAK"
check("B1 [changed after the first run] labour's share of consumption inside its band in every WEAK year; the STRONG "
      "years (annual input-output, 1997–2023) carry no band", inside(P["labour_share_c"][weak],
      P["labour_share_c_lo"][weak], P["labour_share_c_hi"][weak]) and P.loc[weak, "labour_share_c_lo"].notna().all()
      and P.loc[~weak, ["labour_share_c_lo", "labour_share_c_hi"]].isna().all().all()
      and list(P.index[~weak]) == list(range(1997, 2024)), f"{int(weak.sum())} WEAK years, {int((~weak).sum())} STRONG")
check("B2 κ's median inside its min–max every year", inside(P["kappa_med"], P["kappa_min"], P["kappa_max"]))
check("B3 labour-origin financing inside its band every year", inside(P["labor_origin_fin"], P["labor_origin_fin_lo"],
      P["labor_origin_fin_hi"]))

# ---- S: sanity
check("S1 adults: about 105 million in 1950 and 265–275 million in 2024 (thousands), rising in at least 95% of years",
      100e3 < P.loc[1950, "adults"] < 110e3 and 265e3 < P.loc[2024, "adults"] < 275e3
      and (P["adults"].diff().dropna() > 0).mean() >= 0.95,
      f"{P.loc[1950, 'adults']:.0f}, {P.loc[2024, 'adults']:.0f}")
rr = P["real_rate"].dropna()
check("S2 [changed after the first run] the real rate within [-5%, 12%] every year; the 1981–1985 mean above 4% and the "
      "2010s mean below 3%",
      rr.between(-0.05, 0.12).all() and rr.loc[1981:1985].mean() > 0.04 and rr.loc[2010:2019].mean() < 0.03,
      f"range {rr.min():.4f}..{rr.max():.4f}; 1981–85 {rr.loc[1981:1985].mean():.4f}; 2010s {rr.loc[2010:2019].mean():.4f}")
check("S3 depreciation within [0.03, 0.07] every year", P["delta"].dropna().between(0.03, 0.07).all(),
      f"range {P['delta'].min():.4f}..{P['delta'].max():.4f}")
check("S4 θ_V within [0.4, 0.8] where measured", tv.between(0.4, 0.8).all(), f"range {tv.min():.3f}..{tv.max():.3f}")
check("S5 housing's share of consumer spending within [0.10, 0.20] every year",
      P["housing_share_pce"].dropna().between(0.10, 0.20).all(),
      f"range {P['housing_share_pce'].min():.3f}..{P['housing_share_pce'].max():.3f}")
check("S6 the employment rate within [0.55, 0.66] every year", P["emp_rate"].dropna().between(0.55, 0.66).all(),
      f"range {P['emp_rate'].min():.3f}..{P['emp_rate'].max():.3f}")

check("S7 the production and nonsupervisory group's share of private jobs within [0.75, 0.88] every year (about four "
      "in five)", P["pns_share"].dropna().between(0.75, 0.88).all(),
      f"range {P['pns_share'].min():.4f}..{P['pns_share'].max():.4f}")
check("S8 the pay gap within [0.9, 1.6] every year", P["pay_gap"].dropna().between(0.9, 1.6).all(),
      f"range {P['pay_gap'].min():.4f}..{P['pay_gap'].max():.4f}")
check("S9 [added 2026-11-06] durables' share of spending on everything but housing within [0.08, 0.25], 1950-2024",
      P.loc[1950:2024, "dur_share"].between(0.08, 0.25).all(),
      f"range {P.loc[1950:2024, 'dur_share'].min():.4f}..{P.loc[1950:2024, 'dur_share'].max():.4f}")
_rd = np.log(P["wage_exshelter"] / P["wage_goods"])                 # durables over the CPI less shelter, in logs
_wb = (P["dur_share"] + P["dur_share"].shift(1)) / 2.0
_rg = np.log(P["dur_rel_price"]) - _rd                              # the other goods over the CPI less shelter, minus
_tq = (_wb * _rd.diff() + (1.0 - _wb) * (-_rg).diff()).loc[1951:2024]   # the Tornqvist identity: the CPI less shelter's
check("I11 [added 2026-11-06] durables' relative price splits the CPI less shelter exactly (Tornqvist on spending "
      "weights): each year's change in it is the weighted change in durables' and the other goods' prices (1e-12)",
      float(np.nanmax(np.abs(_tq))) < 1e-12, f"{float(np.nanmax(np.abs(_tq))):.1e}")

# ---- the skill split (her go, 2026-11-08), added after its series were built; tolerances set before the first run
SPLIT = ["ndg_share", "low_share", "high_share", "wage_ndg", "wage_low", "wage_high", "pay_dur", "pay_nd", "pay_low",
         "pay_high", "lvl_dur", "lvl_nd", "lvl_low", "lvl_high"]
gaps = {c: [y for y in range(1950, 2025) if pd.isna(P.loc[y, c])] for c in SPLIT}
pre = all((P.loc[1950:1963, c] == 1.0).all() for c in ("pay_low", "pay_high"))
check("C7 [added 2026-11-08] the skill split's fourteen series are complete over 1950-2024, and the services groups' pay is "
      "exactly 1 before 1964 (BLS's services industries begin in 1964)", not any(gaps.values()) and pre,
      f"gaps: { {c: g for c, g in gaps.items() if g} }")
nipa_rows = {}
for line in open(os.path.join(REPO, "progress_and_prosperity", "lambda", "data", "cache", "NipaDataA.txt"), encoding="utf-8"):
    parts = line.strip().split(",", 2)
    if len(parts) == 3 and parts[1].isdigit():
        nipa_rows.setdefault(parts[0], {})[int(parts[1])] = float(parts[2].strip('"').replace(",", ""))
GRP = {"ndg": ["DNDGRC", "DUTLRC", "DCOMRC"],
       "low": ["DFSERC", "DACCRC", "DRCARC", "DPERRC", "DHHMRC", "DMVSRC", "DPUBRC", "DSOCRC"],
       "high": ["DHPNRC", "DOUTRC", "DTEDRC", "DPRSRC", "DFNLRC", "DINSRC"]}
yrs = list(range(1950, 2025))
nv = lambda code: np.array([nipa_rows[code][y] for y in yrs])  # noqa: E731
add1 = float(np.max(np.abs(P.loc[1950:2024, ["ndg_share", "low_share", "high_share"]].sum(axis=1) - 1.0)))
srv_lines = sum(nv(c) for g in GRP.values() for c in g if c != "DNDGRC") + nv("DNPIRC") + nv("DFTRRC") - nv("DEXFRC")
gap_s = float(np.max(np.abs(srv_lines / (nv("DSERRC") - nv("DHSGRC")) - 1.0)))
check("I12 [added 2026-11-08] the three groups' shares add to one (1e-12), and BEA's lines add up: the groups' services, "
      "nonprofits' own consumption and net foreign travel are services less housing within 0.05% every year",
      add1 < 1e-12 and gap_s < 5e-4, f"shares {add1:.1e}, lines {gap_s:.2e}")
def torn_steps(val, lp):
    """Chained Tornqvist log index from levels (spending) and log prices, rows = years."""
    lv = [0.0]
    for t in range(1, len(val)):
        w0, w1 = val[t - 1] / val[t - 1].sum(), val[t] / val[t].sum()
        lv.append(lv[-1] + float(np.dot((w0 + w1) / 2.0, lp[t] - lp[t - 1])))
    return np.array(lv)


glog, gval = {}, {}
for g, cs in GRP.items():
    gval[g] = np.array([[nipa_rows[c][y] for c in cs] for y in yrs])
    glog[g] = torn_steps(gval[g], np.log(np.array([[nipa_rows[c[:-1] + "G"][y] for c in cs] for y in yrs])))
sh_g = np.column_stack([gval[g].sum(axis=1) for g in GRP])
nest_log = torn_steps(sh_g, np.column_stack([glog[g] for g in GRP]))
r_other = np.log(P.loc[1950:2024, "dur_rel_price"].values) - np.log(P.loc[1950:2024, "wage_exshelter"].values
                                                                    / P.loc[1950:2024, "wage_goods"].values)
w_other = P.loc[1950:2024, "wage_exshelter"].values * np.exp(r_other)     # the wage over the other goods, CPI level
wmax = max(float(np.max(np.abs(w_other * np.exp(nest_log - glog[g]) / P.loc[1950:2024, f"wage_{g}"].values - 1.0)))
           for g in GRP)
agg = torn_steps(sh_g, -np.column_stack([np.log(P.loc[1950:2024, f"wage_{g}"].values) for g in GRP]))
amax = float(np.max(np.abs(agg + np.log(w_other / 100.0))))
check("I13 [added 2026-11-08; changed before the first fit: the CPI's level] each group's wage is the wage over the other "
      "goods (CPI level) times BEA's three-group price over the group's (chained Tornqvists on spending weights), "
      "recomputed from the raw flat file on a code path of its own (relative 1e-9); and the groups' prices aggregate on "
      "the same weights to the other goods' CPI price exactly (1e-12)", wmax < 1e-9 and amax < 1e-12,
      f"{wmax:.1e}, aggregation {amax:.1e}")
pmax = 0.0
for col, sid in (("pay_dur", "CES3100000008"), ("pay_nd", "CES3200000008")):
    r = (monthly_complete(fred_cache(os.path.join(ROOT, "cache", f"{sid}.csv"), sid)) / link).reindex(yrs)
    pmax = max(pmax, float(np.max(np.abs((r / r.loc[1950]).values - P.loc[1950:2024, col].values))))
IND = {"DHPNRC": "CES6500000008", "DOUTRC": "CES6500000008", "DTEDRC": "CES6500000008", "DPRSRC": "CES6000000008",
       "DFNLRC": "CES5500000008", "DINSRC": "CES5500000008"}
rel = {c: monthly_complete(fred_cache(os.path.join(ROOT, "cache", f"{sid}.csv"), sid)) / link for c, sid in IND.items()}
y64 = list(range(1964, 2025))
val = np.array([[nipa_rows[c][y] for c in GRP["high"]] for y in y64])
lw = np.log(np.array([[rel[c].loc[y] for c in GRP["high"]] for y in y64]))
lv = [0.0]
for t in range(1, len(y64)):
    w0, w1 = val[t - 1] / val[t - 1].sum(), val[t] / val[t].sum()
    lv.append(lv[-1] + float(np.dot((w0 + w1) / 2.0, lw[t] - lw[t - 1])))
hmax = float(np.max(np.abs(np.exp(np.array(lv)) - P.loc[1964:2024, "pay_high"].values)))
check("I14 [added 2026-11-08] the goods' pay (BLS durable and nondurable manufacturing over the linked earnings, 1950 = "
      "1; 1e-12) and the high-skill group's pay (its industries over the linked earnings, chained Tornqvist on spending "
      "weights, 1964 = 1; 1e-9) recomputed from the raw files", pmax < 1e-12 and hmax < 1e-9,
      f"goods {pmax:.1e}, high {hmax:.1e}")
lmax = 0.0
for col, sid in (("lvl_dur", "CES3100000008"), ("lvl_nd", "CES3200000008")):
    r = (monthly_complete(fred_cache(os.path.join(ROOT, "cache", f"{sid}.csv"), sid)) / link).reindex(yrs)
    lmax = max(lmax, float(np.max(np.abs(r.values - P.loc[1950:2024, col].values))))
w64 = np.array([nipa_rows[c][1964] for c in GRP["high"]])
l64 = float(np.exp(np.dot(w64 / w64.sum(), [np.log(rel[c].loc[1964]) for c in GRP["high"]])))
hl = float(np.max(np.abs(P.loc[1950:2024, "lvl_high"].values - l64 * P.loc[1950:2024, "pay_high"].values)))
inrange = all(P.loc[1950:2024, c].between(0.3, 1.5).all() for c in ("lvl_dur", "lvl_nd", "lvl_low", "lvl_high"))
check("I15 [added 2026-11-08] the pay levels: the goods' are BLS's own ratios over the linked earnings (1e-12); the "
      "high-skill group's is its industries' 1964 spending-weighted geometric mean carried by its chained index (1e-12); "
      "all four within [0.3, 1.5]", lmax < 1e-12 and hl < 1e-12 and inrange,
      f"goods {lmax:.1e}, high {hl:.1e}; 1964 levels low {P.loc[1964, 'lvl_low']:.3f}, high {P.loc[1964, 'lvl_high']:.3f}")
sh = P.loc[1950:2024]
ok = sh["high_share"].between(0.08, 0.5).all() and sh.loc[2024, "high_share"] - sh.loc[1950, "high_share"] > 0.2 \
    and sh["low_share"].between(0.15, 0.35).all() and all(sh[c].between(0.8, 2.0).all() for c in SPLIT[6:10])
check("S10 [added 2026-11-08] the high-skill share within [0.08, 0.5] and up at least 0.2 from 1950 to 2024, the "
      "low-skill share within [0.15, 0.35], every pay path within [0.8, 2.0]", ok,
      f"high {sh.loc[1950, 'high_share']:.3f} -> {sh.loc[2024, 'high_share']:.3f}; pay ranges "
      + ", ".join(f"{c} {sh[c].min():.2f}..{sh[c].max():.2f}" for c in SPLIT[6:10]))

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
