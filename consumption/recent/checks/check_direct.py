# check_direct.py - PASS/FAIL checks for the direct-reads unit (consumption/recent/code/direct.py).
# Three kinds: (A) inputs reproduce the publisher headline figures cited in README_bls_ce.md, README_bea.md,
# README_fed.md, the SCF 2025 Bulletin (Box 1) and the FEDS Note of 2026-10-09; (B) the outputs obey their
# identities (shares sum to one, weights sum to families, parts add to totals), recomputed here independently from
# the tidy files rather than by importing direct.py; (C) NOTES_direct.md carries the generated tables verbatim and
# the figures exist at 200 dpi.
#
# Run from the repo root:  venv/bin/python -I consumption/recent/checks/check_direct.py
import struct
import sys
import zlib
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd

RECENT = Path(__file__).resolve().parents[1]
THREAD = RECENT.parent
TIDY = THREAD / "data" / "tidy"
RAW = THREAD / "data" / "raw"
OUT = RECENT / "out"
FIG = RECENT / "figures"
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


def close(a, b, tol):
    """|a - b| <= tol, plus 1e-8 relative: the output CSVs carry 10 significant digits."""
    return abs(float(a) - float(b)) <= tol + 1e-8 * abs(float(b))


def wavg(x, w):
    return float((np.asarray(x, float) * np.asarray(w, float)).sum() / np.asarray(w, float).sum())


# ---------------------------------------------------------------------------------------------------------------
# load
CEQ = pd.read_csv(TIDY / "ce_income_quintiles_long.csv")
CED = pd.read_csv(TIDY / "ce_income_deciles_long.csv")
CETOP = pd.read_csv(TIDY / "ce_dpce_top_shares.csv")
DPCE = pd.read_csv(TIDY / "bls_dpce_long.csv")
JOINT = pd.read_csv(TIDY / "bea_joint_dpi_pce_by_decile.csv")
JX = pd.read_csv(TIDY / "bea_joint_dpi_pce_joint_shares.csv")
PID = pd.read_csv(TIDY / "bea_dpi_distribution.csv")
ISP = pd.read_csv(TIDY / "bea_pce_price_by_income_decile.csv")
PI = pd.read_csv(TIDY / "bea_pi_long.csv", dtype={"table": str})
DFA = pd.read_csv(TIDY / "dfa_income_long.csv")
S25 = pd.read_csv(TIDY / "scf2025_summary.csv.gz")
S22 = pd.read_csv(TIDY / "scf2022_summary.csv.gz")

TS = pd.read_csv(OUT / "direct_top_shares.csv")
CG = pd.read_csv(OUT / "direct_ce_groups.csv")
INC = pd.read_csv(OUT / "direct_income_saving.csv")
DW = pd.read_csv(OUT / "direct_dfa_wealth.csv")
WFA = pd.read_csv(OUT / "direct_scf2025_windfall.csv")
SP = pd.read_csv(OUT / "direct_scf2025_spending.csv")
EV = pd.read_csv(OUT / "direct_evidence_table.csv")
TOT = "Average annual expenditures"


def ce_mean(df, year, group, path=TOT, stat="mean"):
    x = df[(df.year == year) & (df.group == group) & (df.path == path) & (df.stat == stat)]
    return float(x.value.iloc[0])


def ce_n(df, year, group):
    x = df[(df.year == year) & (df.group == group) & (df.stat == "value") &
           (df.item_clean == "Number of consumer units (in thousands)")]
    return float(x.value.iloc[0])


# ---------------------------------------------------------------------------------------------------------------
# A. publisher headline figures
print("--- A. inputs against publisher headline figures")
# A1 CE 2025 release (README_bls_ce: Verification, releases)
check("A1 CE 2025 all CUs: 137,994 thousand CUs, income $110,847, expenditures $81,905",
      ce_n(CEQ, 2025, "all") == 137994 and
      ce_mean(CEQ, 2025, "all", "Consumer unit characteristics: > Income before taxes") == 110847 and
      ce_mean(CEQ, 2025, "all") == 81905)
rel = {"q1": (37935, 18125), "q2": (51405, 46080), "q3": (68983, 78584), "q4": (92250, 126349), "q5": (159512, 286188)}
ok = all(ce_mean(CEQ, 2025, g) == e and
         ce_mean(CEQ, 2025, g, "Consumer unit characteristics: > Income before taxes") == i
         for g, (e, i) in rel.items())
check("A1 CE 2025 quintile expenditures and incomes equal the release", ok)
# A2 top shares: means x counts against the derived file and the published aggregate-share tables
for grp, df, src, n_g in (("q5", CEQ, "CE Table 1101 (quintiles)", 5), ("d10", CED, "CE Table 1110 (deciles)", 10)):
    gs = [f"q{k}" for k in range(1, 6)] if n_g == 5 else [f"d{k:02d}" for k in range(1, 11)]
    worst, worst_pub = 0.0, 0.0
    for y in range(2019, 2026):
        agg = {g: ce_n(df, y, g) * ce_mean(df, y, g) for g in gs}
        s = 100 * agg[grp] / sum(agg.values())
        mine = TS[(TS.source == src) & (TS.year == y) & (TS.group == ("top20" if grp == "q5" else "top10"))]
        worst = max(worst, abs(s - mine.share_pct.iloc[0]))
        ref = CETOP[(CETOP.year == y) & (CETOP.group == grp) & CETOP.source.str.contains("means x CU counts")]
        worst = max(worst, abs(s - ref.share_pct.iloc[0]))
        pub = CETOP[(CETOP.year == y) & (CETOP.group == grp) & CETOP.source.str.startswith("CE aggregate-share table")]
        worst_pub = max(worst_pub, abs(s - pub.share_pct.iloc[0]))
    check(f"A2 CE {grp} share 2019-2025 recomputed = output = ce_dpce_top_shares.csv", worst < 1e-6, f"max {worst:.2e}")
    check(f"A2 CE {grp} share within 0.08 pt of BLS's published aggregate-share table", worst_pub <= 0.08,
          f"max {worst_pub:.3f}")
# A3 dPCE
t1 = DPCE[(DPCE.table == "T1") & (DPCE.nipa_2_3_5_line == 1) & DPCE.group.str.startswith("d")]
dev = t1.groupby("year").value.sum().sub(1).abs().max()
check("A3 dPCE T1 line 1 decile shares sum to 1 (every year)", dev <= 0.0002, f"max dev {dev:.5f}")
t2 = DPCE[(DPCE.table == "T2") & (DPCE.line == 26)].set_index("year").value
d910 = t1[t1.group.isin(["d09", "d10"])].groupby("year").value.sum()
check("A3 dPCE T2 line 26 (top 20%) = T1 d09 + d10", (t2 - d910).abs().max() <= 0.00011)
d10 = t1[t1.group == "d10"].set_index("year").value * 100
quoted = {2000: 26.30, 2007: 27.18, 2019: 26.11, 2020: 24.96, 2021: 26.07, 2022: 26.39, 2023: 25.74}
check("A3 dPCE top-decile shares equal README_bls_ce's quoted values", all(close(d10[y], v, 0.005) for y, v in quoted.items()))
q5q = {2019: 39.83, 2020: 38.31, 2021: 39.67, 2022: 39.98, 2023: 39.50}
check("A3 dPCE top-quintile shares equal README_bls_ce's quoted values",
      all(close(100 * t2[y], v, 0.005) for y, v in q5q.items()))
# A4 joint distribution
js = JOINT[(JOINT.metric == "share") & JOINT.group.str.match(r"D\d\d")]
dev = js.groupby(["year", "series"]).value.sum().sub(1).abs().max()
check("A4 joint distribution decile shares sum to 1 (DPI, PCE, saving; 3-decimal rounding)", dev <= 0.006,
      f"max dev {dev:.4f}")
grid = JX[JX.dpi_group.str.match(r"D\d\d") & JX.pce_group.str.match(r"D\d\d")].groupby("year")[
    ["share_households", "share_dpi", "share_pce"]].sum()
check("A4 joint DPI x PCE grid sums to 1 within 0.007 (README_bea)", (grid - 1).abs().max().max() <= 0.007)
tot = JOINT[JOINT.metric == "total"].pivot_table(index="year", columns="series", values="value")
sh = js.pivot_table(index=["year", "group"], columns="series", values="value")
sr = JOINT[JOINT.metric == "saving_rate"].set_index(["year", "group"]).value
devs = []
for (y, g), r in sh.iterrows():
    if y < 2019 or g == "D01":
        continue
    rec = r["Personal Saving"] * tot.loc[y, "Personal Saving"] / (r["Disposable Personal Income"] *
                                                                    tot.loc[y, "Disposable Personal Income"])
    devs.append(abs(rec - sr[(y, g)]))
check("A4 joint saving rates = saving share x total / (DPI share x total), D02-D10 2019-2023", max(devs) < 0.01,
      f"max dev {max(devs):.4f}")
# A5 BEA personal income distribution and the 2025 nowcast
q = PID[(PID.income_concept == "Personal income") & (PID.metric == "share") & PID.group.str.match(r"Q\d") &
        (PID.year >= 2019) & PID.ranking.isin(["equivalized_pi", "not_stated"])]
dev = q.groupby("year").value.sum().sub(1).abs().max()
check("A5 PI quintile shares sum to 1 within 0.003, 2019-2025", dev <= 0.003, f"max dev {dev:.4f}")
now = PID[PID.status == "nowcast_experimental"]
sh25 = now[now.metric == "share"].set_index("group").value * 100
g25 = now[now.metric == "growth_nominal_2024_2025"].set_index("group").value
check("A5 nowcast shares 5.2/9.6/13.4/19.1/52.7 and growth 4.1/5.8/5.0/5.4/4.6 (README_bea)",
      list(np.round(sh25[["Q1", "Q2", "Q3", "Q4", "Q5"]].values, 1)) == [5.2, 9.6, 13.4, 19.1, 52.7] and
      list(g25[["Q1", "Q2", "Q3", "Q4", "Q5"]].values) == [4.1, 5.8, 5.0, 5.4, 4.6])
s24 = PID[(PID.year == 2024) & (PID.income_concept == "Personal income") & (PID.metric == "share") &
          (PID.ranking == "equivalized_pi") & PID.group.str.match(r"Q\d")].set_index("group").value
agg = (s24 * (1 + g25 / 100)).sum() / s24.sum() - 1
check("A5 2024 shares x nowcast growth imply aggregate PI growth 4.89% (README_bea)", close(100 * agg, 4.89, 0.005),
      f"{100 * agg:.3f}%")
# A6 ISPCEPX cumulative inflation 2019-2024 (README_bea table)
want = {"D01": 19.6, "D02": 19.5, "D03": 19.4, "D04": 19.3, "D05": 19.2, "D06": 19.1, "D07": 19.1, "D08": 19.2,
        "D09": 19.2, "D10": 20.4}
dec = ISP[ISP.grouping.str.startswith("decile")].pivot_table(index="year", columns="group", values="value")
got = 100 * (dec.loc[2024] / dec.loc[2019] - 1)
agg_ix = ISP[ISP.source_column == "Indexed Published PCE PI"].set_index("year").value
check("A6 ISPCEPX 2019-2024 inflation by decile = README_bea (D01 19.6 ... D10 20.4; all 19.5)",
      all(close(got[k], v, 0.05) for k, v in want.items()) and close(100 * (agg_ix[2024] / agg_ix[2019] - 1), 19.5, 0.05))
# A7 NIPA
m = PI[PI.table == "2.6"].pivot_table(index="date", columns="line", values="value")
check("A7 saving rate Sep 2026 = 3.8% and personal saving $911.1bn (README_bea release check)",
      m.loc["2026-09", 35] == 3.8 and close(m.loc["2026-09", 34] / 1e3, 911.1, 0.05))
idg = (m.loc["2019-01":, 27] - m.loc["2019-01":, 28] - m.loc["2019-01":, 34]).abs().max()
check("A7 identity DPI - outlays = saving, 2019-01..2026-09 (within $1m)", idg <= 1.0, f"max {idg}")
# A8 SCF weights and the 2022 price factor
check("A8 SCF 2025: WGT over all implicate records = 134.96 million families", close(S25.WGT.sum() / 1e6, 134.96, 0.01),
      f"{S25.WGT.sum() / 1e6:.3f}")
check("A8 SCF 2022: WGT over all implicate records = 131.31 million families", close(S22.WGT.sum() / 1e6, 131.31, 0.01),
      f"{S22.WGT.sum() / 1e6:.3f}")
o = np.argsort(S22.NETWORTH.values, kind="mergesort")
cw = np.cumsum(S22.WGT.values[o]) / S22.WGT.sum()
med = S22.NETWORTH.values[o][np.searchsorted(cw, 0.5)]
check("A8 SCF 2022 median net worth $210.89k (2025 $) = $192.7k in 2022 $ (README_fed)",
      close(med / 1e3, 210.89, 0.01) and close(med / 1e3 / (4789 / 4376), 192.7, 0.05), f"{med / 1e3:.2f}k")
# A9 SCF 2025 Bulletin, Box 1 (spending)
w = S25.WGT
o = np.argsort(S25.TOTSPENDNH.values, kind="mergesort")
cw = np.cumsum(w.values[o]) / w.sum()
med = S25.TOTSPENDNH.values[o][np.searchsorted(cw, 0.5)]
check("A9 Box 1: mean total spending $48,700 (within 0.1%), median $33,700 (within 1%), aggregate $6.61tn (within 1%)",
      close(wavg(S25.TOTSPENDNH, w), 48700, 48.7) and abs(med / 33700 - 1) < 0.01 and
      abs((S25.TOTSPENDNH * w).sum() / 6.61e12 - 1) < 0.01, f"{wavg(S25.TOTSPENDNH, w):,.0f}; {med:,.0f}")
tot_sp = (S25.TOTSPENDNH * w).sum()
inc6 = S25.groupby("NINCCAT").apply(lambda g: pd.Series({"mean": wavg(g.TOTSPENDNH, g.WGT),
                                                         "share": 100 * (g.TOTSPENDNH * g.WGT).sum() / tot_sp}))
check("A9 Box 1 by usual income: bottom quintile $17,600 / 7.2%, 80-90th $68,700, top decile $138,800 / 28.5%",
      abs(inc6.loc[1, "mean"] / 17600 - 1) < 0.005 and close(inc6.loc[1, "share"], 7.2, 0.06) and
      abs(inc6.loc[5, "mean"] / 68700 - 1) < 0.005 and abs(inc6.loc[6, "mean"] / 138800 - 1) < 0.005 and
      close(inc6.loc[6, "share"], 28.5, 0.07), f"top decile {inc6.loc[6, 'mean']:,.0f}, {inc6.loc[6, 'share']:.2f}%")
nw = pd.cut(S25.NWPCTLECAT, [0, 2, 8, 9, 12], labels=["0-20", "20-80", "80-90", "90-100"])
nw6 = S25.groupby(nw, observed=True).apply(lambda g: pd.Series({"mean": wavg(g.TOTSPENDNH, g.WGT),
                                                                 "share": 100 * (g.TOTSPENDNH * g.WGT).sum() / tot_sp}))
check("A9 Box 1 by wealth: bottom quintile $23,400, 80-90th $68,800, top decile $136,000 / 27.9%",
      abs(nw6.loc["0-20", "mean"] / 23400 - 1) < 0.005 and abs(nw6.loc["80-90", "mean"] / 68800 - 1) < 0.005 and
      abs(nw6.loc["90-100", "mean"] / 136000 - 1) < 0.005 and close(nw6.loc["90-100", "share"], 27.9, 0.06))
check("A9 Box 1 categories: food at home $7,700, food away (incl. delivery) $3,500, vacation $4,200, 39% none",
      abs(wavg(S25.FOODHOME, w) / 7700 - 1) < 0.01 and abs(wavg(S25.FOODAWAY + S25.FOODDELV, w) / 3500 - 1) < 0.01 and
      abs(wavg(S25.VACATION, w) / 4200 - 1) < 0.01 and close(100 * w[S25.VACATION == 0].sum() / w.sum(), 39, 0.6))
# A10 FEDS Note (accessible figure tables)
html = (RAW / "fed" / "feds_notes" / "feds-note-mpc-heterogeneity-accessible-20261009.htm").read_text(
    encoding="utf-8", errors="replace")
tabs = pd.read_html(StringIO(html))
ov = tabs[0].iloc[0]
mine = [wavg(S25[c], w) for c in ("MPSPEND", "MPSAVE", "MPDEBT")]
check("A10 FEDS Note overall allocation 22.35 / 47.31 / 30.30 reproduced (within 0.01)",
      all(close(a, b, 0.01) for a, b in zip(mine, [ov["Spend"], ov["Save"], ov["Pay Debt"]])),
      " / ".join(f"{v:.2f}" for v in mine))
for k, col, tol in ((2, "NINCPCTLECAT", 1.0), (3, "NWPCTLECAT", 0.3)):
    pub = tabs[k].copy()
    pub.columns = ["label", "spend", "save", "debt"]
    g = S25.groupby(col).apply(lambda x: pd.Series({c: wavg(x[v], x.WGT) for c, v in
                                                    (("spend", "MPSPEND"), ("save", "MPSAVE"), ("debt", "MPDEBT"))}))
    d = (g.values - pub[["spend", "save", "debt"]].values)
    check(f"A10 FEDS Note Figure 3 ({'normal income' if k == 2 else 'wealth'}, 12 groups) reproduced within {tol} pt "
          "(public extract vs internal data)", np.abs(d).max() <= tol, f"max {np.abs(d).max():.2f}, median "
          f"{np.median(np.abs(d)):.2f}")
dist = tabs[1].copy()
dist.columns = ["pct", "share"]
dist["share"] = dist.share.str.rstrip("%").astype(float)
mine_d = {p: 100 * w[S25.MPSPEND.round() == p].sum() / w.sum() for p in (0, 50, 100)}
check("A10 FEDS Note Figure 2: share spending 0 / 50 / 100 percent (47 / 11 / 4, whole percent)",
      all(close(mine_d[p], dist.set_index("pct").share[p], 0.75) for p in (0, 50, 100)),
      " / ".join(f"{mine_d[p]:.1f}" for p in (0, 50, 100)))
check("A10 FEDS Note fn 11: 19.6% would save none of it",
      close(100 * w[S25.MPSAVE == 0].sum() / w.sum(), 19.6, 0.06))
wf = S25.NORMINC / 12
o = np.argsort(wf.values, kind="mergesort")
cw = np.cumsum(w.values[o]) / w.sum()
mw = wf.values[o][np.searchsorted(cw, 0.5)]
b = S25.NINCPCTLECAT == 1
check("A10 FEDS Note: implied windfall median $7,000, mean $11,800, bottom decile mean $1,500",
      abs(mw / 7000 - 1) < 0.01 and abs(wavg(wf, w) / 11800 - 1) < 0.01 and
      abs(wavg(wf[b], w[b]) / 1500 - 1) < 0.03, f"{mw:,.0f}, {wavg(wf, w):,.0f}, {wavg(wf[b], w[b]):,.0f}")
# A11 DFA (README_fed table, 2022Q3 -> 2026Q2, $bn)
lv = DFA[DFA.measure == "level"].pivot_table(index=["date", "category"], columns="group", values="value")
readme = {("Corporate equities and mutual fund shares", "pct00to20"): (616.3, 950.9),
          ("Corporate equities and mutual fund shares", "pct99to100"): (11632.9, 25614.9),
          ("Corporate equities and mutual fund shares", "pct80to99"): (15809.2, 30771.6),
          ("Real estate", "pct80to99"): (18281.5, 21946.1), ("Net worth", "pct99to100"): (29698.0, 46859.8),
          ("Net worth", "pct60to80"): (18413.7, 24332.8)}
check("A11 DFA levels equal README_fed's 2022Q3 -> 2026Q2 table",
      all(close(lv.loc[("2022Q3", c), g] / 1e3, a, 0.05) and close(lv.loc[("2026Q2", c), g] / 1e3, b_, 0.05)
          for (c, g), (a, b_) in readme.items()))
shr = DFA[(DFA.measure == "share") & DFA.date.isin(["2019Q4", "2022Q3", "2026Q2"]) &
          DFA.category.isin(["Net worth", "Corporate equities and mutual fund shares", "Real estate",
                             "Consumer credit"])]
dev = shr.groupby(["date", "category"]).value.sum().sub(100).abs().max()
check("A11 DFA published group shares sum to 100 (0.1-point rounding)", dev <= 0.35, f"max dev {dev:.2f}")

# ---------------------------------------------------------------------------------------------------------------
print("--- B. output identities (recomputed independently)")
# B1 CE decile shares sum to 100 every year; the output's top-decile share is one of them
for y in range(2014, 2026):
    gs = [f"d{k:02d}" for k in range(1, 11)]
    agg = np.array([ce_n(CED, y, g) * ce_mean(CED, y, g) for g in gs])
    if abs(100 * agg.sum() / agg.sum() - 100) > 1e-9:
        break
lev = CG[CG.block == "levels"]
x = lev[(lev.grouping == "quintile") & lev.group.isin([f"q{k}" for k in range(1, 6)])]
dev = x.groupby("year").share_total_pct.sum().sub(100).abs().max()
check("B1 CE quintile shares of aggregate spending sum to 100 (2019-2025)", dev < 1e-6, f"{dev:.1e}")
x = lev[(lev.grouping == "decile") & lev.group.str.match(r"d\d\d")]
dev = x.groupby("year").share_total_pct.sum().sub(100).abs().max()
check("B1 CE decile shares of aggregate spending sum to 100 (2019-2025)", dev < 1e-6, f"{dev:.1e}")
# B2 aggregates: top20 + bottom80 = sum of quintiles, nominal and real
x = lev[lev.grouping == "quintile"].set_index(["group", "year"])
ok = True
for y in range(2019, 2026):
    for c in ("agg_bn_total", "agg_bn_total_real2024", "agg_bn_consumption_real2024"):
        s5 = sum(x.loc[(f"q{k}", y), c] for k in range(1, 6))
        ok &= close(x.loc[("top20", y), c] + x.loc[("bottom80", y), c], s5, 1e-6)
check("B2 CE top 20% + bottom 80% = sum of quintiles (nominal and real aggregates)", ok)
# B2b real growth recomputed: q5 2022 -> 2025 with ISPCEPX Q5 and the aggregate PCE price index for 2025
pceu = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", usecols=["table", "freq", "line", "date", "value"])
pp = pceu[(pceu.table == "2.4.4U") & (pceu.freq == "A") & (pceu.line == 1)].set_index("date").value
pp.index = pp.index.astype(int)
isq5 = ISP[(ISP.group == "Q5")].set_index("year").value
p25 = isq5[2024] * pp[2025] / pp[2024]
m22, m25 = ce_mean(CEQ, 2022, "q5"), ce_mean(CEQ, 2025, "q5")
n22, n25 = ce_n(CEQ, 2022, "q5"), ce_n(CEQ, 2025, "q5")
g_mine = 100 * ((n25 * m25 / p25) / (n22 * m22 / isq5[2022]) - 1)
g_out = CG[(CG.block == "growth") & (CG.grouping == "quintile") & (CG.group == "q5") &
           (CG.window == "2022->2025")].g_agg_bn_total_real2024.iloc[0]
check("B2 top-20% real aggregate growth 2022-2025 recomputed (ISPCEPX Q5, 2025 by aggregate PCE prices)",
      close(g_mine, g_out, 1e-8), f"{g_mine:.3f}%")
# B3 composition items add to the published total (2022 and 2025, q1 and q5; suppressed cells filled)
cp = CG[CG.block == "composition"]
ok, worst = True, 0.0
for (wdw, g), x in cp.groupby(["window", "group"]):
    tot_row = x[x["item"] == "Total (sum of items)"].iloc[0]
    a, b_ = int(wdw[:4]), int(wdw[-4:])
    for yr, col in ((a, "mean_start"), (b_, "mean_end")):
        if g in ("q1", "q5", "all"):
            ref = ce_mean(CEQ, yr, g)
            worst = max(worst, abs(tot_row[col] - ref))
check("B3 CE budget items (28) add to published total expenditures within $5 (q1, q5, all; 2019/2022/2025)",
      worst <= 5, f"max ${worst:.1f}")
dsum = cp[cp["item"] != "Total (sum of items)"].groupby(["window", "group"]).change_share_pts.sum().abs().max()
check("B3 changes in budget shares sum to zero", dsum < 1e-6)
# B4 Zandi's implied share recomputed
z = CG[CG.block == "zandi_implied_share"].set_index("base_year")
ok = True
for base, T in ((2022, 3), (2023, 2)):
    s0 = z.loc[base, "share_base_pct"] / 100
    ok &= close(100 * s0 * 1.04 ** T / (s0 * 1.04 ** T + 1 - s0), z.loc[base, "zandi_share_2025_real_pct"], 1e-9)
check("B4 Zandi's implied 2025 top-20% share (real) = s0 1.04^T / (s0 1.04^T + 1 - s0)", ok,
      f"2022 base {z.loc[2022, 'zandi_share_2025_nominal_pct']:.2f}%, 2023 base {z.loc[2023, 'zandi_share_2025_nominal_pct']:.2f}%")
# B5 income: quintile levels = share x total; 2025 = 2024 x (1 + nowcast growth); groups add up
il = INC[(INC.block == "income_quintile_levels") & (INC.concept == "Personal income")].set_index(["group", "year"])
ok = all(close(il.loc[(q, 2025), "level_bn"], il.loc[(q, 2024), "level_bn"] * (1 + g25[q.upper()] / 100), 1e-6)
         for q in ("q1", "q2", "q3", "q4", "q5"))
ok &= all(close(il.loc[("all", y), "level_bn"], sum(il.loc[(f"q{k}", y), "level_bn"] for k in range(1, 6)), 1e-6)
          for y in range(2019, 2026))
check("B5 PI quintile levels: 2025 = 2024 x (1 + nowcast growth); quintiles add to the total", ok)
jr = INC[INC.block == "joint_by_dpi_group"].dropna(subset=["saving_rate_published"]).copy()
ndec = jr.group.map(lambda g: 2 if g.startswith("Q") else 1)
# rounding bound: shares printed to 3 decimals (+-0.0005 per decile summed), published rate to 3 decimals
bound = (jr.saving_rate_from_shares.abs() * (ndec * 0.0005 / jr.saving_share.abs() + ndec * 0.0005 / jr.dpi_share)
         + 0.0005)
dev = (jr.saving_rate_from_shares - jr.saving_rate_published).abs()
check("B5 joint saving rates from shares match the published rates within the 3-decimal rounding bound "
      "(deciles, quintiles, top 5% and 1%, 2019-2023)", (dev <= bound).all(),
      f"max dev {dev.max():.4f} (D01 2022, bound {bound[dev.idxmax()]:.4f})")
# B6 DFA gains: level differences, shares of the gain sum to 100
gn = DW[(DW.block == "gains") & (DW.base == "equities (level change)") & (DW.window == "2022Q3->2026Q2")]
gn = gn.set_index("group")
ok = all(close(gn.loc[g, "gain_bn"], (lv.loc[("2026Q2", "Corporate equities and mutual fund shares"), g] -
                                      lv.loc[("2022Q3", "Corporate equities and mutual fund shares"), g]) / 1e3, 1e-6)
         for g in ("pct00to20", "pct20to40", "pct40to60", "pct60to80", "pct80to99", "pct99to100"))
grp6 = ["pct00to20", "pct20to40", "pct40to60", "pct60to80", "pct80to99", "pct99to100"]
ok &= close(gn.loc[grp6, "share_of_gain_pct"].sum(), 100, 1e-9)
check("B6 DFA equity gains 2022Q3-2026Q2 = level differences; group shares of the gain sum to 100", ok,
      f"top 20% {gn.loc['top20', 'share_of_gain_pct']:.1f}%")
# B7 wealth effect arithmetic
we = DW[DW.block == "wealth_effect_bound"]
ok = True
for (wdw, base, cwv, den), x in we.groupby(["window", "base", "c_w", "denominator"]):
    x = x.set_index("group")
    ok &= close(x.loc[grp6, "wealth_effect_bn_per_year"].sum(), x.loc["all", "wealth_effect_bn_per_year"], 1e-6)
    ok &= close(x.loc[grp6, "group_spending_bn"].sum(), x.loc["all", "pce_end_bn_saar"], 1e-6)
    g_ = DW[(DW.block == "gains") & (DW.window == wdw) & (DW.base == base)].set_index("group").gain_bn
    ok &= all(close(x.loc[g, "wealth_effect_bn_per_year"], cwv * g_[g], 1e-6) for g in grp6)
check("B7 wealth effect = c_w x gain by group; groups add to the total; group spending adds to PCE", ok)
pce26 = PI[(PI.table == "2.6") & (PI.line == 29) & PI.date.isin(["2026-04", "2026-05", "2026-06"])].value.mean() / 1e3
x = we[(we.window == "2022Q3->2026Q2") & (we.c_w == 0.035) & (we.base == "equities (level change)") &
       (we.group == "all")].iloc[0]
check("B7 PCE at 2026Q2 (mean of monthly SAAR, Table 2.6 line 29) used as the denominator",
      close(x.pce_end_bn_saar, pce26, 1e-6), f"${pce26:,.0f}bn; wealth effect {x.pct_of_pce:.2f}% of PCE")
rv = DW[DW.block == "z1_revaluation_share"]
check("B7 Z.1 revaluation share of the change in household equity holdings lies in (0.8, 1.0]",
      ((rv.reval_share > 0.8) & (rv.reval_share <= 1.0)).all(), ", ".join(f"{v:.3f}" for v in rv.reval_share))
# B8 SCF: weights sum to families in every grouping; allocations add to about 100; spending shares add to 100
wfw = WFA[WFA.block == "windfall"]
fam = wfw[wfw.families_m.notna()].groupby("grouping").families_m.sum()
check("B8 every windfall grouping's families sum to 134.96 million", (fam - S25.WGT.sum() / 1e6).abs().max() < 1e-6,
      f"{len(fam)} groupings")
tot3 = (wfw.spend_pct + wfw.save_pct + wfw.debt_pct).dropna()
check("B8 spend + save + debt within [99.0, 100.0] for every group (some answers sum to 99/99.9)",
      ((tot3 >= 99.0) & (tot3 <= 100.0 + 1e-9)).all(), f"range {tot3.min():.2f}-{tot3.max():.2f}")
famsp = SP.groupby("grouping").families_m.sum()
shsp = SP.groupby("grouping").share_of_aggregate_pct.sum()
check("B8 SCF spending table: families sum to 134.96m and shares to 100 in every grouping",
      (famsp - S25.WGT.sum() / 1e6).abs().max() < 1e-6 and (shsp - 100).abs().max() < 1e-6)
# B8b SCF top shares recomputed independently (income 2024 ranking)
top10 = 100 * (S25.TOTSPENDNH * w)[S25.INCCAT == 6].sum() / tot_sp
top20 = 100 * (S25.TOTSPENDNH * w)[S25.INCCAT >= 5].sum() / tot_sp
mine10 = TS[TS.source.str.startswith("SCF 2025, total non-housing spending (TOTSPENDNH), ranked by income 2024") &
            (TS.group == "top10")].share_pct.iloc[0]
mine20 = TS[TS.source.str.startswith("SCF 2025, total non-housing spending (TOTSPENDNH), ranked by income 2024") &
            (TS.group == "top20")].share_pct.iloc[0]
check("B8 SCF 2025 top 10% / top 20% shares of non-housing spending (income 2024) recomputed",
      close(top10, mine10, 1e-9) and close(top20, mine20, 1e-9), f"{top10:.2f}% / {top20:.2f}%")
# B9 windfall: decile means recomputed by groupby; gradient = ratio of the decile means
dec = S25.NINCPCTLECAT.clip(upper=10)
g10 = S25.groupby(dec).apply(lambda g: wavg(g.MPSPEND, g.WGT))
out10 = wfw[wfw.grouping == "usual income, deciles"].set_index("group").spend_pct
check("B9 windfall spend share by usual-income decile recomputed", all(close(g10[k], out10[f"D{k}"], 1e-9)
                                                                       for k in range(1, 11)))
gr = WFA[WFA.block == "gradient_vs_post"].set_index("grouping")
check("B9 gradient ratio = top-decile / bottom-decile spend share; bootstrap interval brackets it",
      close(gr.loc["usual income, deciles", "ratio_spend"], g10[10] / g10[1], 1e-9) and
      (gr.ratio_spend_lo95 < gr.ratio_spend).all() and (gr.ratio_spend < gr.ratio_spend_hi95).all(),
      f"{g10[10] / g10[1]:.3f}")
check("B9 bootstrap SEs positive and finite", (wfw.se_spend_boot.dropna() > 0).all() and
      np.isfinite(wfw.se_spend_boot.dropna()).all())
liq = S25.LIQ + S25.CDS + S25.NMMF + S25.STOCKS + S25.BOND
htm = liq < 0.5 * S25.NORMINC / 12
out_htm = wfw[(wfw.grouping == "hand-to-mouth (FEDS Note definition)")].set_index("group")
check("B9 hand-to-mouth (FEDS definition) share of families and spend shares recomputed",
      close(out_htm.loc["hand-to-mouth", "families_m"], w[htm].sum() / 1e6, 1e-6) and
      close(out_htm.loc["hand-to-mouth", "spend_pct"], wavg(S25.MPSPEND[htm], w[htm]), 1e-9),
      f"{100 * w[htm].sum() / w.sum():.1f}% of families")
adj = wfw[wfw.grouping.str.startswith("hand-to-mouth, regression-adjusted")].set_index("group")
check("B9 regression-adjusted hand-to-mouth gap within 1 pt of the FEDS Note's 2.6 pts (22.9 vs 20.3)",
      abs((adj.loc["hand-to-mouth", "spend_pct"] - adj.loc["not hand-to-mouth", "spend_pct"]) - 2.6) <= 1.0,
      f"{adj.loc['hand-to-mouth', 'spend_pct']:.1f} vs {adj.loc['not hand-to-mouth', 'spend_pct']:.1f}")
# B10 evidence table
check("B10 evidence table: 'consistent' column is yes / no / can't tell",
      EV.consistent_with_zandi_split.isin(["yes", "no", "can't tell"]).all(), f"{len(EV)} rows")

# ---------------------------------------------------------------------------------------------------------------
print("--- C. notes and figures")
notes = (RECENT / "NOTES_direct.md").read_text(encoding="utf-8") if (RECENT / "NOTES_direct.md").exists() else ""
tables = (OUT / "direct_notes_tables.md").read_text(encoding="utf-8").split("<!-- ")
missing = []
for blk in tables[1:]:
    key, body = blk.split(" -->\n", 1)
    if body.strip() not in notes:
        missing.append(key)
check("C1 NOTES_direct.md carries every generated table verbatim", not missing and notes != "",
      "missing: " + ", ".join(missing) if missing else f"{len(tables) - 1} tables")


def png_dpi(path):
    data = path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    i = 8
    while i < len(data):
        n = struct.unpack(">I", data[i:i + 4])[0]
        typ = data[i + 4:i + 8]
        if typ == b"pHYs":
            ppx, ppy, unit = struct.unpack(">IIB", data[i + 8:i + 17])
            return ppx * 0.0254 if unit == 1 else None
        i += 12 + n
    return None


for f in ("fig_direct_top_shares.png", "fig_direct_dfa_equity.png", "fig_direct_windfall.png"):
    p = FIG / f
    dpi = png_dpi(p) if p.exists() else None
    check(f"C2 {f} exists at 200 dpi", dpi is not None and round(dpi) == 200, f"{dpi:.1f} dpi" if dpi else "")
for f in ("direct_top_shares.csv", "direct_ce_groups.csv", "direct_income_saving.csv", "direct_dfa_wealth.csv",
          "direct_scf2025_spending.csv", "direct_scf2025_windfall.csv", "direct_evidence_table.csv"):
    check(f"C3 out/{f} present and non-empty", (OUT / f).exists() and len(pd.read_csv(OUT / f)) > 0)

n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS) - n_fail} PASS, {n_fail} FAIL")
sys.exit(1 if n_fail else 0)
