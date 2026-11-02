# direct.py - Q2, direct reads: what the official distributions themselves say about who is doing the
# spending (consumption/recent; Stella's question 2, third angle beside sectors.py and fingerprint.py).
#
# The claim weighed (Mark Zandi, Moody's, EconoFact Chats, 2026-07-24; consumption/data/raw/other/): over about
# three years real spending of the top 20% of the income distribution grew close to 4% a year and that of the
# bottom 80% close to zero; spending growth depends on a small group whose wealth rides AI-driven equity gains;
# lower-middle households have drawn down savings. Moody's own distributional numbers (for example a top-decile
# spending share near one half) are not public data and are not used here.
#
# Six reads, all from vendored official files (consumption/data/tidy, documented in README_bls_ce.md,
# README_bea.md, README_fed.md):
#   1. Top spending shares over time, every official source on one footing (CE, BLS dPCE, BEA-BLS joint, SCF).
#   2. CE 2019-2025 by quintile and decile: nominal and real means, growth, Zandi's implied share, budget shifts.
#   3. Income side: BEA personal income by quintile (2025 nowcast) and disposable income by quintile (to 2024, what
#      spending is paid from), taxes by group, joint-distribution saving rates by DPI decile, the saving rate.
#   4. Wealth side: DFA by income group; equity gains since 2022Q3; an assumption-driven wealth-effect bound.
#   5. SCF 2025 windfall question by income, wealth and liquidity: the MPC gradient the post assumes.
#   6. Evidence table and the generated tables pasted into NOTES_direct.md.
#
# Run from the repo root:  venv/bin/python -I consumption/recent/code/direct.py      (about 15 s)
# Outputs: consumption/recent/out/direct_*.csv, out/direct_notes_tables.md, figures/fig_direct_*.png.
# Checks:  consumption/recent/checks/check_direct.py.
# Plain functions plus top-level code, so each block can be pasted into a notebook cell.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                      # consumption/recent/code
sys.path.insert(0, str(HERE.parents[1] / "code"))          # consumption/code (common.py)

import io
import zipfile
from io import StringIO

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

import common

RECENT = HERE.parent
OUT = RECENT / "out"
FIG = RECENT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
TIDY = common.TIDY
RAW = common.RAW

SEED = 20261102
N_BOOT = 400                                   # family bootstrap replicates for the SCF windfall means
ZANDI_TOP, ZANDI_B80 = 0.04, 0.0              # Zandi: top 20% ~4%/yr real, bottom 80% ~0
CW = {"low": 0.02, "central": 0.035, "high": 0.05}   # the post's wealth-effect range (Fig 0, fn 31), Figs 8-10 use 0.035
POST_MPC_BOTTOM, POST_MPC_TOP = 1.0, (0.40, 0.65)    # the post's MPC schedule (Fig 0 box, fn 27): permanent flow
QS = ["q1", "q2", "q3", "q4", "q5"]
DS = [f"d{k:02d}" for k in range(1, 11)]
DFA_GROUPS = ["pct00to20", "pct20to40", "pct40to60", "pct60to80", "pct80to99", "pct99to100"]
DFA_LABEL = {"pct00to20": "0-20", "pct20to40": "20-40", "pct40to60": "40-60", "pct60to80": "60-80",
             "pct80to99": "80-99", "pct99to100": "99-100"}
# SCF 12 percentile groups (INCPCTLECAT etc.): 1=<10, ..., 9=80-89.9, 10=90-94.9, 11=95-98.9, 12=99-100
PCT12_LABEL = {1: "0-10", 2: "10-20", 3: "20-30", 4: "30-40", 5: "40-50", 6: "50-60", 7: "60-70", 8: "70-80",
               9: "80-90", 10: "90-95", 11: "95-99", 12: "99-100"}
PCT12_TO_DEC = {k: min(k, 10) for k in range(1, 13)}
PCT12_TO_DFA = {1: "pct00to20", 2: "pct00to20", 3: "pct20to40", 4: "pct20to40", 5: "pct40to60", 6: "pct40to60",
                7: "pct60to80", 8: "pct60to80", 9: "pct80to99", 10: "pct80to99", 11: "pct80to99", 12: "pct99to100"}
CAT6_LABEL = {1: "0-20", 2: "20-40", 3: "40-60", 4: "60-80", 5: "80-90", 6: "90-100"}


def write_csv(df, name):
    df.to_csv(OUT / name, index=False, float_format="%.10g")
    return OUT / name


def wmean(x, w):
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    return float((x * w).sum() / w.sum())


def wquantile(x, w, q):
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    o = np.argsort(x, kind="mergesort")
    cw = np.cumsum(w[o]) / w.sum()
    return float(x[o][np.searchsorted(cw, q)])


# %% 0. the publisher's analysis of the SCF windfall question (vendored once through common.fetch; offline after)
FEDS_NOTE = "feds_notes/feds-note-mpc-heterogeneity-20261009.html"
FEDS_ACC = "feds_notes/feds-note-mpc-heterogeneity-accessible-20261009.htm"
common.fetch("fed", FEDS_NOTE,
             "https://www.federalreserve.gov/econres/notes/feds-notes/heterogeneity-in-the-marginal-propensity-to-"
             "consume-among-u-s-households-20261009.html",
             "FEDS Note (Aladangady, Bricker, Chang, Goodman, Li, 2026-10-09), Heterogeneity in the Marginal Propensity "
             "to Consume Among U.S. Households; doi 10.17016/2380-7172.4197; the Board analysis of the SCF 2025 "
             "windfall question (X9375-X9377)",
             "Q2 direct reads: publisher figures for the SCF 2025 windfall tabulation (consumption/recent/code/direct.py)")
common.fetch("fed", FEDS_ACC,
             "https://www.federalreserve.gov/econres/notes/feds-notes/heterogeneity-in-the-marginal-propensity-to-"
             "consume-among-u-s-households-accessible-20261009.htm",
             "Accessible version (figure data tables) of the FEDS Note Heterogeneity in the Marginal Propensity to "
             "Consume Among U.S. Households (2026-10-09): Figures 1-8 and A1 as HTML tables",
             "Q2 direct reads: publisher windfall allocations by income and wealth group, checked in "
             "consumption/recent/checks/check_direct.py")


def feds_tables():
    """The accessible version's figure tables: overall mean, spend-share distribution, by normal income, by wealth,
    and the regression-adjusted hand-to-mouth means."""
    html = (RAW / "fed" / FEDS_ACC).read_text(encoding="utf-8", errors="replace")
    t = pd.read_html(StringIO(html))
    by_inc, by_nw = t[2].copy(), t[3].copy()
    for x in (by_inc, by_nw):
        x.columns = ["label", "spend", "save", "debt"]
        x["pct12"] = range(1, 13)
    return {"overall": t[0], "dist": t[1], "by_normal_income": by_inc, "by_wealth": by_nw, "htm": t[4],
            "htm_wealth": t[5]}


FEDS = feds_tables()

# %% 1. load the tidy files
CE_D = pd.read_csv(TIDY / "ce_income_deciles_long.csv")
CE_Q = pd.read_csv(TIDY / "ce_income_quintiles_long.csv")
CE_AGG = pd.read_csv(TIDY / "ce_income_aggshare_long.csv")
CE_TOP = pd.read_csv(TIDY / "ce_dpce_top_shares.csv")
DPCE = pd.read_csv(TIDY / "bls_dpce_long.csv")
JOINT = pd.read_csv(TIDY / "bea_joint_dpi_pce_by_decile.csv")
JOINT_X = pd.read_csv(TIDY / "bea_joint_dpi_pce_joint_shares.csv")
PIDIST = pd.read_csv(TIDY / "bea_dpi_distribution.csv")
ISP = pd.read_csv(TIDY / "bea_pce_price_by_income_decile.csv")
PI = pd.read_csv(TIDY / "bea_pi_long.csv", dtype={"table": str})
PCEU = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", usecols=["table", "freq", "line", "date", "value"])
PCEU = PCEU[(PCEU.line == 1)].copy()
DFA = pd.read_csv(TIDY / "dfa_income_long.csv")
SCF25 = pd.read_csv(TIDY / "scf2025_summary.csv.gz")
SCF22 = pd.read_csv(TIDY / "scf2022_summary.csv.gz")
SCF22_PRICE = 4789 / 4376                     # the 2022 extract is in 2025 dollars (README_fed item 5)

# the post's wealth-effect propensity as transcribed (post_published_numbers.csv): Fig 0 and footnote 31 say 2-5 cents
# per dollar per year (P051/P052), the body text "three to five cents" (P570/P571), Figs 8-10 use c_w = 0.035 (P618)
POSTN = pd.read_csv(TIDY / "post_published_numbers.csv").set_index("id")
POST_CW_FIG0 = (float(POSTN.loc["P051", "value"]), float(POSTN.loc["P052", "value"]))      # cents
POST_CW_BODY = (float(POSTN.loc["P570", "value"]), float(POSTN.loc["P571", "value"]))      # cents
POST_CW_FIGS = float(POSTN.loc["P618", "value"])                                            # per year
assert (round(100 * CW["low"], 9), round(100 * CW["high"], 9)) == POST_CW_FIG0 and CW["central"] == POST_CW_FIGS

# aggregate PCE price index, annual, current NIPA vintage (2026-10-29): 2.4.4U line 1
PCE_PI_A = PCEU[(PCEU.table == "2.4.4U") & (PCEU.freq == "A")].assign(year=lambda x: x.date.astype(int))
PCE_PI_A = PCE_PI_A.set_index("year").value
PCE_INFL_2025 = PCE_PI_A[2025] / PCE_PI_A[2024]       # used to carry every ISPCEPX group index into 2025


def pi_series(line, freq="M"):
    t = "2.6" if freq == "M" else "2.1"
    x = PI[(PI.table == t) & (PI.line == line)][["date", "value"]].copy()
    return x.set_index("date").value


PCE_M = pi_series(29)          # PCE, $ million SAAR, monthly
PCE_A = pi_series(29, "A")     # PCE, $ million, annual


def pce_quarter(q):
    """Average of the three monthly SAAR values of PCE in quarter 'YYYYQn', $ billion."""
    y, n = int(q[:4]), int(q[-1])
    months = [f"{y}-{3 * (n - 1) + k:02d}" for k in (1, 2, 3)]
    return PCE_M.loc[months].mean() / 1e3


# %% 2. CE helpers
def ce_cell(df, year, group, path, stat="mean"):
    x = df[(df.year == year) & (df.group == group) & (df.path == path) & (df.stat == stat)]
    if len(x) != 1:
        return np.nan
    return float(x.value.iloc[0])


def ce_counts(df, year):
    x = df[(df.year == year) & (df.item_clean == "Number of consumer units (in thousands)") & (df.stat == "value")]
    return x.set_index("group").value


TOT = "Average annual expenditures"
PIP = "Average annual expenditures > Personal insurance and pensions"
CASH = "Average annual expenditures > Cash contributions"


def ce_fill_suppressed(df, year, path, groups):
    """Group means for one item with suppressed (RSE >= 25%) cells filled from the all-CU identity
    N_all m_all = sum_g N_g m_g: the residual spread equally per CU over the suppressed groups (exact when one
    cell is suppressed, up to the tables' rounding). Returns (series of means, list of filled groups)."""
    n = ce_counts(df, year)
    m = pd.Series({g: ce_cell(df, year, g, path) for g in groups})
    miss = list(m.index[m.isna()])
    if miss:
        m_all = ce_cell(df, year, "all", path)
        resid = n["all"] * m_all - (n[groups].drop(miss) * m.drop(miss)).sum()
        m.loc[miss] = resid / n[miss].sum()
    return m, miss


def ce_group_table(df, years, groups, kind):
    """Per year and group: CU count (thousands), mean total expenditures, mean of the consumption-like total
    (total minus personal insurance and pensions minus cash contributions), SE of the total's mean."""
    rows = []
    for y in years:
        n = ce_counts(df, y)
        pip, f1 = ce_fill_suppressed(df, y, PIP, groups)
        cash, f2 = ce_fill_suppressed(df, y, CASH, groups)
        for g in groups + ["all"]:
            tot = ce_cell(df, y, g, TOT)
            if g == "all":
                p_, c_ = ce_cell(df, y, "all", PIP), ce_cell(df, y, "all", CASH)
            else:
                p_, c_ = pip[g], cash[g]
            rows.append(dict(year=y, grouping=kind, group=g, n_cu_thousands=n[g], mean_total=tot,
                             se_total=ce_cell(df, y, g, TOT, "se"), mean_pip=p_, mean_cash=c_,
                             mean_consumption=tot - p_ - c_,
                             filled_from_identity=";".join(sorted(set(f1 + f2) & {g})) if g != "all" else "",
                             income_before_taxes=ce_cell(df, y, g, "Consumer unit characteristics: > Income before taxes")))
    return pd.DataFrame(rows)


CE_QT = ce_group_table(CE_Q, range(2019, 2026), QS, "quintile")
CE_DT = ce_group_table(CE_D, range(2014, 2026), DS, "decile")


def share_with_se(t, top):
    """Share of the top groups in aggregate spending (CU count x mean), and an approximate SE treating the
    group means as independent samples (published BRR SEs; Fay's BRR in 2025)."""
    x = t[t.group != "all"].set_index("group")
    agg = x.n_cu_thousands * x.mean_total
    T = agg.sum()
    s = agg[top].sum() / T
    var = 0.0
    for g in x.index:
        dsdm = x.n_cu_thousands[g] * ((1 - s) if g in top else -s) / T
        var += (dsdm * x.se_total[g]) ** 2
    aggc = x.n_cu_thousands * x.mean_consumption
    sc = aggc[top].sum() / aggc.sum()
    allrow = t[t.group == "all"].iloc[0]
    sc_alt = aggc[top].sum() / (allrow.n_cu_thousands * allrow.mean_consumption)
    return s, np.sqrt(var), sc, sc_alt


# %% 3. Section 1: top shares, every official source on one footing
TS = []
for y in range(2014, 2026):
    t = CE_DT[CE_DT.year == y]
    s, se, sc, sc_alt = share_with_se(t, ["d10"])
    TS.append(dict(source="CE Table 1110 (deciles)", year=y, group="top10", share_pct=100 * s, se_pct=100 * se,
                   share_consumption_pct=100 * sc_alt, method="CU count x mean / sum over deciles"))
    s, se, sc, sc_alt = share_with_se(t, ["d09", "d10"])
    TS.append(dict(source="CE Table 1110 (deciles d09+d10)", year=y, group="top20", share_pct=100 * s,
                   se_pct=100 * se, share_consumption_pct=100 * sc_alt, method="CU count x mean / sum over deciles"))
for y in range(2019, 2026):
    t = CE_QT[CE_QT.year == y]
    s, se, sc, sc_alt = share_with_se(t, ["q5"])
    TS.append(dict(source="CE Table 1101 (quintiles)", year=y, group="top20", share_pct=100 * s, se_pct=100 * se,
                   share_consumption_pct=100 * sc_alt, method="CU count x mean / sum over quintiles"))
for gr, grp, src in (("deciles", "d10", "CE aggregate-share table (deciles), published"),
                     ("quintiles", "q5", "CE aggregate-share table (quintiles), published")):
    x = CE_AGG[(CE_AGG.grouping == gr) & (CE_AGG.item_clean == "Annual aggregate expenditures") &
               (CE_AGG.group == grp)]
    for r in x.itertuples():
        TS.append(dict(source=src, year=r.year, group="top10" if grp == "d10" else "top20", share_pct=r.value,
                       method="as published (0.1 point)"))
d1 = DPCE[(DPCE.table == "T1") & (DPCE.nipa_2_3_5_line == 1) & (DPCE.group == "d10")]
for r in d1.itertuples():
    TS.append(dict(source="BLS distributional PCE (T1 line 1)", year=r.year, group="top10", share_pct=100 * r.value,
                   method="decile share of total PCE"))
d2 = DPCE[(DPCE.table == "T2") & (DPCE.line == 26)]
for r in d2.itertuples():
    TS.append(dict(source="BLS distributional PCE (T2 line 26)", year=r.year, group="top20",
                   share_pct=100 * r.value, method="80-100% share of total (unequivalized) PCE"))
for key, rows_ in (("top1", 28), ("top5", 29)):
    d3 = DPCE[(DPCE.table == "T2") & (DPCE.line == rows_)]
    for r in d3.itertuples():
        TS.append(dict(source="BLS distributional PCE (T2)", year=r.year, group=key, share_pct=100 * r.value,
                       method=f"T2 line {rows_}, share of total (unequivalized) PCE"))
jp = JOINT[(JOINT.series == "Personal Consumption Expenditures") & (JOINT.metric == "share")]
jp = jp.pivot_table(index="year", columns="group", values="value")
for y, r in jp.iterrows():
    TS.append(dict(source="BEA-BLS joint distribution (PCE by DPI decile)", year=y, group="top10",
                   share_pct=100 * r["D10"], method="PCE share of D10 (3-decimal shares)"))
    TS.append(dict(source="BEA-BLS joint distribution (PCE by DPI decile)", year=y, group="top20",
                   share_pct=100 * (r["D09"] + r["D10"]), method="PCE share of D09+D10"))
    TS.append(dict(source="BEA-BLS joint distribution (PCE by DPI decile)", year=y, group="top1",
                   share_pct=100 * r["T01"], method="PCE share of the top 1% by DPI"))
    TS.append(dict(source="BEA-BLS joint distribution (PCE by DPI decile)", year=y, group="top5",
                   share_pct=100 * r["T05"], method="PCE share of the top 5% by DPI"))


def scf_share(df, var_spend, cat, top, w="WGT"):
    s = df[var_spend] * df[w]
    return 100 * s[df[cat].isin(top)].sum() / s.sum()


S = SCF25.copy()
S["SPEND_RENT"] = S.TOTSPENDNH + 12 * S.RENT
S["DEC_INC"] = S.INCPCTLECAT.map(PCT12_TO_DEC)
S["DEC_NINC"] = S.NINCPCTLECAT.map(PCT12_TO_DEC)
S["DEC_NW"] = S.NWPCTLECAT.map(PCT12_TO_DEC)
for var, lab in (("TOTSPENDNH", "total non-housing spending (TOTSPENDNH)"),
                 ("SPEND_RENT", "TOTSPENDNH + 12 x monthly rent")):
    for cat, rk in (("INCCAT", "income 2024 (INCOME)"), ("NINCCAT", "usual income (NORMINC)")):
        TS.append(dict(source=f"SCF 2025, {lab}, ranked by {rk}", year=2025, group="top10",
                       share_pct=scf_share(S, var, cat, [6]), method="WGT over all implicates"))
        TS.append(dict(source=f"SCF 2025, {lab}, ranked by {rk}", year=2025, group="top20",
                       share_pct=scf_share(S, var, cat, [5, 6]), method="WGT over all implicates"))
    for cat, rk in (("INCPCTLECAT", "income 2024 (INCOME)"), ("NINCPCTLECAT", "usual income (NORMINC)")):
        TS.append(dict(source=f"SCF 2025, {lab}, ranked by {rk}", year=2025, group="top1",
                       share_pct=scf_share(S, var, cat, [12]), method="WGT over all implicates"))
        TS.append(dict(source=f"SCF 2025, {lab}, ranked by {rk}", year=2025, group="top5",
                       share_pct=scf_share(S, var, cat, [11, 12]), method="WGT over all implicates"))
TS.append(dict(source="SCF 2025, total non-housing spending (TOTSPENDNH), ranked by net worth", year=2025,
               group="top10", share_pct=scf_share(S, "TOTSPENDNH", "NWPCTLECAT", [10, 11, 12]),
               method="WGT over all implicates"))
# CE on a scope close to the SCF question (TOTSPENDNH excludes rent, mortgage and loan payments, investments and
# retirement contributions): total minus owned and rented dwellings, personal insurance and pensions, and cash
# contributions; denominator all-CU count x mean (avoids the 2022-23 suppressed decile cells)
OWN = "Average annual expenditures > Housing > Shelter > Owned dwellings"
RNT = "Average annual expenditures > Housing > Shelter > Rented dwellings"


def ce_scf_scope_share(df, year, top):
    n = ce_counts(df, year)
    def scope(g):
        return (ce_cell(df, year, g, TOT) - ce_cell(df, year, g, OWN) - ce_cell(df, year, g, RNT) -
                ce_cell(df, year, g, PIP) - ce_cell(df, year, g, CASH))
    return 100 * sum(n[g] * scope(g) for g in top) / (n["all"] * scope("all"))


def ce_scf_scope_share_groups(df, year, top, groups):
    """The same share with the sum over groups as the denominator, as for the other CE shares (suppressed cells
    filled from the all-CU identity): used only to bound the effect of the choice of denominator."""
    n = ce_counts(df, year)
    parts = [ce_fill_suppressed(df, year, p, groups)[0] for p in (TOT, OWN, RNT, PIP, CASH)]
    scope = parts[0] - parts[1] - parts[2] - parts[3] - parts[4]
    return 100 * (n[top] * scope[top]).sum() / (n[groups] * scope[groups]).sum()


SCOPE_DENOM_DIFF = 0.0
for y in range(2019, 2026):
    TS.append(dict(source="CE Table 1110 (deciles), SCF-like scope", year=y, group="top10",
                   share_pct=ce_scf_scope_share(CE_D, y, ["d10"]),
                   method="total minus owned and rented dwellings, pensions and insurance, cash contributions"))
    TS.append(dict(source="CE Table 1101 (quintiles), SCF-like scope", year=y, group="top20",
                   share_pct=ce_scf_scope_share(CE_Q, y, ["q5"]),
                   method="total minus owned and rented dwellings, pensions and insurance, cash contributions"))
    SCOPE_DENOM_DIFF = max(SCOPE_DENOM_DIFF,
                           abs(ce_scf_scope_share(CE_D, y, ["d10"]) - ce_scf_scope_share_groups(CE_D, y, ["d10"], DS)),
                           abs(ce_scf_scope_share(CE_Q, y, ["q5"]) - ce_scf_scope_share_groups(CE_Q, y, ["q5"], QS)))
TS = pd.DataFrame(TS)

FOOTING = {
    "CE": dict(ranking="income before taxes (money income, past 12 months)", equivalized="no",
               unit="consumer unit (CU), CU-weighted groups", scope="CE out-of-pocket expenditures incl. personal "
               "insurance and pensions and cash contributions; employer- and government-paid health care, imputed "
               "rent and FISIM not included", top_tail="survey as collected; under-covers the very top (no "
               "oversample, top-coding, nonresponse rising with income)"),
    "dPCE": dict(ranking="total PCE per CU / sqrt(CU size) (spending, not income)", equivalized="yes",
                 unit="CU, CU-weighted deciles (finlwt21)", scope="all of PCE (national accounts), CE-allocated with "
                 "imputations for out-of-scope items (third-party health care, FISIM, imputed rent)",
                 top_tail="Pareto adjustment of the top 5% of spenders"),
    "joint": dict(ranking="disposable personal income per household / sqrt(size) (CPS-based)", equivalized="yes",
                  unit="household (CPS), household-weighted deciles", scope="all of PCE, allocated by BLS CE-based "
                  "shares matched to BEA's DPI distribution", top_tail="DPI top tail from BEA's income distribution "
                  "(tax-data adjusted); PCE side from the CE (BLS dPCE methods)"),
    "SCF": dict(ranking="family income in 2024 (INCOME), or usual income (NORMINC)", equivalized="no",
                unit="family (primary economic unit), WGT over all implicates", scope="total non-housing spending "
                "over the past 12 months as reported (excludes rent, mortgage and loan payments, investments, "
                "retirement contributions)", top_tail="list-sample oversample of wealthy families (Forbes 400 "
                "excluded); one question on total spending"),
}


def footing_of(src):
    if src.startswith("CE"):
        return FOOTING["CE"]
    if src.startswith("BLS"):
        return FOOTING["dPCE"]
    if src.startswith("BEA"):
        return FOOTING["joint"]
    return FOOTING["SCF"]


for c in ("ranking", "equivalized", "unit", "scope", "top_tail"):
    TS[c] = TS.source.map(lambda s: footing_of(s)[c])
TS = TS[["source", "ranking", "equivalized", "unit", "scope", "top_tail", "year", "group", "share_pct", "se_pct",
         "share_consumption_pct", "method"]]
write_csv(TS, "direct_top_shares.csv")
print("Section 1 done:", len(TS), "rows; SCF-like scope, all-CU vs sum-over-groups denominator: max "
      f"{SCOPE_DENOM_DIFF:.3f} pt")


def ts(source, group, year):
    x = TS[(TS.source == source) & (TS.group == group) & (TS.year == year)]
    return float(x.share_pct.iloc[0])


CEQ, CED = "CE Table 1101 (quintiles)", "CE Table 1110 (deciles)"
DP1, DP2 = "BLS distributional PCE (T1 line 1)", "BLS distributional PCE (T2 line 26)"
JNT = "BEA-BLS joint distribution (PCE by DPI decile)"
SCF_MAIN = "SCF 2025, total non-housing spending (TOTSPENDNH), ranked by income 2024 (INCOME)"

# %% 4. Section 2: CE 2019-2025 by quintile and decile (nominal, real, growth, Zandi's share, budget shifts)
def isp_index(group):
    """ISPCEPX (BEA, June 2026; deciles/quintiles of equivalized DPI, 2000=100) for a CE group, 2019-2025, with
    2025 carried forward by the aggregate PCE price index (2.4.4U line 1, current vintage): no differential
    inflation is assumed for 2025, the one year ISPCEPX does not cover."""
    if group == "all":
        x = ISP[(ISP.source_column == "Indexed Published PCE PI")]
    else:
        kind = "decile" if group.startswith("d") else "quintile"          # CE d01..d10 / q1..q5 -> D01..D10 / Q1..Q5
        x = ISP[(ISP.group == group.upper()) & ISP.grouping.str.startswith(kind)]
    s = x.set_index("year").value.astype(float)
    s.loc[2025] = s.loc[2024] * PCE_INFL_2025
    return s


# ISPCEPX is a PCE-scope deflator (each group's PCE basket over ~150 categories, incl. third-party health care and
# imputed rent), and its 2024 group weights are imputed (2023 shares applied to 2024 category totals; README_bea)
ISP_GROUPS = ISP[ISP.grouping.str.startswith(("decile", "quintile"))]
ISP_2024_IMPUTED = bool(ISP_GROUPS[ISP_GROUPS.year == 2024].imputed_weights.all())
assert ISP_2024_IMPUTED and not ISP[ISP.year < 2024].imputed_weights.any()


def add_real(t):
    t = t.copy()
    p = {g: isp_index(g) for g in t.group.unique()}
    t["price_index_2000eq100"] = [p[g][y] for g, y in zip(t.group, t.year)]
    t["price_2025_carried"] = t.year == 2025
    fac = np.array([p[g][2024] / p[g][y] for g, y in zip(t.group, t.year)])
    for c in ("mean_total", "mean_consumption"):
        t[c + "_real2024"] = t[c] * fac
    t["se_total_real2024"] = t["se_total"] * fac          # the deflator is a constant for the sampling error
    return t


CE_QT = add_real(CE_QT)
CE_DT = add_real(CE_DT[CE_DT.year >= 2019])


def aggregate_groups(t, members, name):
    """Aggregate CE groups: CU-weighted means and aggregates ($ billion), nominal and real (each member deflated by
    its own ISPCEPX group index, then summed)."""
    rows = []
    for y, x in t[t.group.isin(members)].groupby("year"):
        n = x.n_cu_thousands.sum()
        r = dict(year=y, group=name, n_cu_thousands=n)
        for c in ("mean_total", "mean_consumption", "mean_total_real2024", "mean_consumption_real2024"):
            agg = (x.n_cu_thousands * x[c]).sum() / 1e6          # thousands of CUs x $ -> $ billion
            r[c.replace("mean", "agg_bn")] = agg
            r[c] = agg * 1e6 / n
        r["var_agg_total"] = ((x.n_cu_thousands * 1e3 * x.se_total) ** 2).sum()
        r["var_agg_total_real2024"] = ((x.n_cu_thousands * 1e3 * x.se_total_real2024) ** 2).sum()
        rows.append(r)
    return pd.DataFrame(rows)


def group_levels(t, kind, tops):
    base = t.copy()
    base["agg_bn_total"] = base.n_cu_thousands * base.mean_total / 1e6
    base["agg_bn_consumption"] = base.n_cu_thousands * base.mean_consumption / 1e6
    base["agg_bn_total_real2024"] = base.n_cu_thousands * base.mean_total_real2024 / 1e6
    base["agg_bn_consumption_real2024"] = base.n_cu_thousands * base.mean_consumption_real2024 / 1e6
    base["var_agg_total"] = (base.n_cu_thousands * 1e3 * base.se_total) ** 2
    base["var_agg_total_real2024"] = (base.n_cu_thousands * 1e3 * base.se_total_real2024) ** 2
    extra = [aggregate_groups(t, m, nm) for nm, m in tops.items()]
    out = pd.concat([base] + extra, ignore_index=True)
    out["grouping"] = kind
    tot = out[out.group == "all"].set_index("year")
    out["share_total_pct"] = 100 * out.agg_bn_total / out.year.map(
        out[out.group.isin(QS if kind == "quintile" else DS)].groupby("year").agg_bn_total.sum())
    out["share_consumption_pct"] = 100 * out.agg_bn_consumption / out.year.map(tot.agg_bn_consumption)
    return out


LEV_Q = group_levels(CE_QT, "quintile", {"top20": ["q5"], "bottom80": QS[:4]})
LEV_D = group_levels(CE_DT, "decile", {"top10": ["d10"], "bottom90": DS[:9], "top20_dec": DS[8:],
                                        "bottom80_dec": DS[:8]})
LEV = pd.concat([LEV_Q, LEV_D], ignore_index=True)

WINDOWS = [(2019, 2025), (2019, 2022), (2022, 2025), (2023, 2025), (2022, 2023), (2023, 2024), (2024, 2025)]
GR = []
for kind, lev in (("quintile", LEV_Q), ("decile", LEV_D)):
    for g, x in lev.groupby("group"):
        x = x.set_index("year")
        for a, b in WINDOWS:
            r = dict(grouping=kind, group=g, window=f"{a}->{b}", years=b - a)
            for c in ("mean_total", "mean_consumption", "mean_total_real2024", "mean_consumption_real2024",
                      "agg_bn_total", "agg_bn_consumption", "agg_bn_total_real2024", "agg_bn_consumption_real2024"):
                r["g_" + c] = 100 * (x.loc[b, c] / x.loc[a, c] - 1)
            # approximate SEs (group means and years independent): the relative SE of each end's aggregate, scaled by
            # the growth factor of the SAME concept. Nominal growth: nominal aggregates and factor. Real growth: each
            # member's SE deflated by its own index, the real aggregates and the real factor (the real factor, not
            # the nominal one, is what multiplies the relative SE of a real ratio).
            ratio = x.loc[b, "agg_bn_total"] / x.loc[a, "agg_bn_total"]
            rel = np.sqrt(x.loc[b, "var_agg_total"] / (x.loc[b, "agg_bn_total"] * 1e9) ** 2 +
                          x.loc[a, "var_agg_total"] / (x.loc[a, "agg_bn_total"] * 1e9) ** 2)
            r["se_g_agg_bn_total"] = 100 * ratio * rel
            ratio_r = x.loc[b, "agg_bn_total_real2024"] / x.loc[a, "agg_bn_total_real2024"]
            rel_r = np.sqrt(x.loc[b, "var_agg_total_real2024"] / (x.loc[b, "agg_bn_total_real2024"] * 1e9) ** 2 +
                            x.loc[a, "var_agg_total_real2024"] / (x.loc[a, "agg_bn_total_real2024"] * 1e9) ** 2)
            r["se_g_agg_bn_total_real2024"] = 100 * ratio_r * rel_r
            GR.append(r)
GR = pd.DataFrame(GR)


def gap_row(kind, top, bot, window):
    t = GR[(GR.grouping == kind) & (GR.group == top) & (GR.window == window)].iloc[0]
    u = GR[(GR.grouping == kind) & (GR.group == bot) & (GR.window == window)].iloc[0]
    T = int(t.years)
    return dict(grouping=kind, top=top, bottom=bot, window=window, years=T,
                gap_real_total_pts=t.g_agg_bn_total_real2024 - u.g_agg_bn_total_real2024,
                gap_real_consumption_pts=t.g_agg_bn_consumption_real2024 - u.g_agg_bn_consumption_real2024,
                gap_nominal_total_pts=t.g_agg_bn_total - u.g_agg_bn_total,
                se_gap_pts=np.hypot(t.se_g_agg_bn_total_real2024, u.se_g_agg_bn_total_real2024),
                top_real_total=t.g_agg_bn_total_real2024, bottom_real_total=u.g_agg_bn_total_real2024,
                top_real_consumption=t.g_agg_bn_consumption_real2024,
                bottom_real_consumption=u.g_agg_bn_consumption_real2024,
                zandi_gap_pts=100 * ((1 + ZANDI_TOP) ** T - (1 + ZANDI_B80) ** T))


GAPS = pd.DataFrame([gap_row("quintile", "top20", "bottom80", w) for w in
                     ("2019->2025", "2019->2022", "2022->2025", "2022->2023", "2023->2025", "2024->2025")] +
                    [gap_row("decile", "top10", "bottom90", w) for w in
                     ("2019->2025", "2022->2025", "2023->2025")])


def zandi_share(base):
    """Top-quintile share of CE aggregate spending in 2025 if, from the base year, real spending of the top 20% grew
    4% a year and the bottom 80%'s not at all; nominal version adds each side's own ISPCEPX inflation."""
    T = 2025 - base
    lq = LEV_Q.set_index(["group", "year"])
    s0 = lq.loc[("q5", base), "share_total_pct"] / 100
    s0c = lq.loc[("q5", base), "share_consumption_pct"] / 100
    pi_top = isp_index("q5")[2025] / isp_index("q5")[base]
    b0, b1 = lq.loc[("bottom80", base)], lq.loc[("bottom80", 2025)]
    pi_bot = (b1.agg_bn_total / b0.agg_bn_total) / (b1.agg_bn_total_real2024 / b0.agg_bn_total_real2024)
    up = (1 + ZANDI_TOP) ** T
    real = s0 * up / (s0 * up + (1 - s0))
    nom = s0 * up * pi_top / (s0 * up * pi_top + (1 - s0) * pi_bot)
    nomc = s0c * up * pi_top / (s0c * up * pi_top + (1 - s0c) * pi_bot)
    obs = lq.loc[("q5", 2025), "share_total_pct"] / 100
    obsc = lq.loc[("q5", 2025), "share_consumption_pct"] / 100
    se0 = TS[(TS.source == "CE Table 1101 (quintiles)") & (TS.year == base)].se_pct.iloc[0]
    se1 = TS[(TS.source == "CE Table 1101 (quintiles)") & (TS.year == 2025)].se_pct.iloc[0]
    return dict(base_year=base, years=T, share_base_pct=100 * s0, zandi_share_2025_real_pct=100 * real,
                zandi_share_2025_nominal_pct=100 * nom, observed_share_2025_pct=100 * obs,
                zandi_minus_observed_pts=100 * (nom - obs), se_change_pts=np.hypot(se0, se1),
                inflation_top_pct=100 * (pi_top - 1), inflation_bottom80_pct=100 * (pi_bot - 1),
                consumption_share_base_pct=100 * s0c, zandi_consumption_share_2025_nominal_pct=100 * nomc,
                observed_consumption_share_2025_pct=100 * obsc)


ZSH = pd.DataFrame([zandi_share(2022), zandi_share(2023)])
ZSH["zandi_minus_observed_in_ses"] = ZSH.zandi_minus_observed_pts / ZSH.se_change_pts


# Zandi's own arithmetic: +4% a year for the top 20% and 0% for the bottom 80% average to 4% x the top-20 share, so
# his 2% aggregate needs a top-20 share of one half; against that, what the CE's own aggregates did a year (real)
def annual(g_cum_pct, years):
    return 100 * ((1 + g_cum_pct / 100) ** (1 / years) - 1)


grq = GR[(GR.grouping == "quintile") & (GR.window == "2022->2025")].set_index("group")
ZARITH = pd.DataFrame(
    [dict(item=f"Zandi's split (top 20% +4%, bottom 80% 0%) averaged with the {lab} top-20 share",
          share_top20_pct=s, pct_a_year=100 * (ZANDI_TOP * s / 100 + ZANDI_B80 * (1 - s / 100)))
     for lab, s in (("CE 2025", ts(CEQ, "top20", 2025)), ("BLS dPCE 2023", ts(DP2, "top20", 2023)),
                    ("SCF 2025", ts(SCF_MAIN, "top20", 2025)))] +
    [dict(item="Top-20 share at which his split averages his 2%", share_top20_pct=100 * 0.02 / ZANDI_TOP,
          pct_a_year=2.0)] +
    [dict(item=f"CE real aggregate spending 2022-2025, {lab}, a year", share_top20_pct=np.nan,
          pct_a_year=annual(grq.loc[g, "g_agg_bn_total_real2024"], 3))
     for g, lab in (("all", "all CUs"), ("top20", "top 20%"), ("bottom80", "bottom 80%"))])

# budget composition 2022 -> 2025 (and 2019 -> 2025) for the bottom and top quintiles, the bottom 80% and all CUs
COMP_ITEMS = [  # (label, regex on the path below 'Average annual expenditures > ')
    ("Food at home", r"^Food > Food at home$"), ("Food away from home", r"^Food > Food away from home$"),
    ("Alcoholic beverages", r"^Alcoholic beverages$"),
    ("Owned dwellings (mortgage interest, property taxes, upkeep)", r"^Housing > Shelter > Owned dwellings$"),
    ("Rented dwellings", r"^Housing > Shelter > Rented dwellings$"),
    ("Other lodging (incl. vacation homes, hotels)", r"^Housing > Shelter > Other lodging$"),
    ("Utilities, fuels, public services", r"^Housing > Utilities, fuels, and public services$"),
    ("Household operations", r"^Housing > Household operations$"),
    ("Housekeeping supplies", r"^Housing > Housekeeping supplies$"),
    ("Household furnishings and equipment", r"^Housing > Household furnishings and equipment$"),
    ("Apparel and services", r"^Apparel and services$"),
    ("Vehicle purchases (net outlay)", r"^Transportation > Vehicle purchases \(net outlay\)$"),
    ("Gasoline and other fuels", r"^Transportation > Gasoline(, other fuels, and motor oil| and other fuels)$"),
    ("Other vehicle expenses", r"^Transportation > Other vehicle expenses$"),
    ("Public and other transportation", r"^Transportation > Public and other transportation$"),
    ("Health insurance", r"^Healthcare > Health insurance$"), ("Medical services", r"^Healthcare > Medical services$"),
    ("Drugs", r"^Healthcare > Drugs$"), ("Medical supplies", r"^Healthcare > Medical supplies$"),
    ("Entertainment", r"^Entertainment$"), ("Personal care", r"^Personal care products and services$"),
    ("Reading", r"^Reading$"), ("Education", r"^Education$"),
    ("Tobacco", r"^Tobacco products and smoking supplies$"), ("Miscellaneous", r"^Miscellaneous$"),
    ("Cash contributions", r"^Cash contributions$"),
    ("Life and other personal insurance", r"^Personal insurance and pensions > Life and other personal insurance$"),
    ("Pensions and Social Security", r"^Personal insurance and pensions > (Retirement, pensions, and Social "
                                     r"Security|Pensions and Social Security)$"),
]


def comp_means(year):
    """Quintile means of each composition item, suppressed cells filled from the all-CU identity."""
    x = CE_Q[(CE_Q.year == year) & (CE_Q.stat == "mean") & CE_Q.path.str.startswith(TOT + " > ")]
    sub = x.path.str.slice(len(TOT) + 3)
    rows = {}
    for lab, rx in COMP_ITEMS:
        hit = x[sub.str.match(rx)].path.unique()
        assert len(hit) == 1, (year, lab, hit)
        m, filled = ce_fill_suppressed(CE_Q, year, hit[0], QS)
        m["all"] = ce_cell(CE_Q, year, "all", hit[0])
        rows[lab] = dict(m, filled=";".join(filled))
    return pd.DataFrame(rows).T


COMP = []
for a, b in ((2022, 2025), (2019, 2025)):
    ma, mb = comp_means(a), comp_means(b)
    na, nb = ce_counts(CE_Q, a), ce_counts(CE_Q, b)
    for g, members in (("q1", ["q1"]), ("q5", ["q5"]), ("bottom80", QS[:4]), ("all", ["all"])):
        def grp(m, n):
            v = (m[members].astype(float) * n[members]).sum(axis=1) / n[members].sum()
            return v
        va, vb = grp(ma, na), grp(mb, nb)
        ta, tb = va.sum(), vb.sum()
        for lab in va.index:
            COMP.append(dict(window=f"{a}->{b}", group=g, item=lab, mean_start=va[lab], mean_end=vb[lab],
                             share_start_pct=100 * va[lab] / ta, share_end_pct=100 * vb[lab] / tb,
                             change_share_pts=100 * (vb[lab] / tb - va[lab] / ta),
                             growth_nominal_pct=100 * (vb[lab] / va[lab] - 1),
                             contribution_pts=100 * (vb[lab] - va[lab]) / ta,
                             filled_cells=";".join(sorted(set((ma.loc[lab, "filled"] + ";" + mb.loc[lab, "filled"])
                                                             .strip(";").split(";")) & set(members) - {""}))))
        COMP.append(dict(window=f"{a}->{b}", group=g, item="Total (sum of items)", mean_start=ta, mean_end=tb,
                         share_start_pct=100.0, share_end_pct=100.0, change_share_pts=0.0,
                         growth_nominal_pct=100 * (tb / ta - 1), contribution_pts=100 * (tb / ta - 1), filled_cells=""))
COMP = pd.DataFrame(COMP)

CEG = pd.concat([
    LEV.assign(block="levels"),
    GR.assign(block="growth"),
    GAPS.assign(block="gap_top_vs_rest"),
    ZSH.assign(block="zandi_implied_share"),
    COMP.assign(block="composition"),
    ZARITH.assign(block="zandi_arithmetic"),
], ignore_index=True)
first = ["block", "grouping", "group", "year", "window", "item"]
CEG = CEG[first + [c for c in CEG.columns if c not in first]]
write_csv(CEG, "direct_ce_groups.csv")
print("Section 2 done:", len(CEG), "rows")

# %% 5. Section 3: income side (BEA personal income by quintile, joint-distribution saving, the saving rate)
def pidist_levels(concept, ranking):
    """Quintile shares and levels ($ billion = share x NIPA total of the June 2026 vintage), 2019-2024; for personal
    income ranked by equivalized personal income the 2025 experimental nowcast is chained on as 2024 level x
    (1 + nowcast growth). Disposable income (PI minus taxes) ends in 2024."""
    sh = PIDIST[(PIDIST.income_concept == concept) & (PIDIST.metric == "share") & (PIDIST.ranking == ranking) &
                PIDIST.group.isin(["Q1", "Q2", "Q3", "Q4", "Q5"]) & (PIDIST.year >= 2019)]
    tot = PIDIST[(PIDIST.income_concept == concept) & (PIDIST.metric == "total")].set_index("year").value
    rows = []
    for r in sh.itertuples():
        rows.append(dict(year=r.year, status=r.status, group=r.group.lower(), share=r.value,
                         total_bn=tot[r.year], level_bn=r.value * tot[r.year]))
    out = pd.DataFrame(rows)
    if concept == "Personal income" and ranking == "equivalized_pi":
        now = PIDIST[(PIDIST.status == "nowcast_experimental")]
        g = now[now.metric == "growth_nominal_2024_2025"].set_index("group").value
        s = now[now.metric == "share"].set_index("group").value
        l24 = out[out.year == 2024].set_index("group").level_bn
        for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
            out.loc[len(out)] = dict(year=2025, status="nowcast_experimental", group=q.lower(), share=s[q],
                                     total_bn=np.nan, level_bn=l24[q.lower()] * (1 + g[q] / 100))
    out["ranking"] = ranking
    out["concept"] = concept
    return out


def add_income_aggregates(t):
    rows = []
    for y, x in t.groupby("year"):
        x = x.set_index("group")
        for nm, mem in (("top20", ["q5"]), ("bottom80", ["q1", "q2", "q3", "q4"]), ("all", QS)):
            rows.append(dict(year=y, status=x.status.iloc[0], group=nm, share=x.loc[mem, "share"].sum(),
                             total_bn=x.total_bn.iloc[0], level_bn=x.loc[mem, "level_bn"].sum(),
                             ranking=x.ranking.iloc[0], concept=x.concept.iloc[0]))
    t = pd.concat([t, pd.DataFrame(rows)], ignore_index=True)
    # real: each quintile by its own ISPCEPX quintile index (2025 carried by aggregate PCE prices, as in section 2)
    real = []
    for r in t.itertuples():
        if r.group in QS:
            p = isp_index(r.group)
            real.append(r.level_bn * p[2024] / p[r.year])
        else:
            real.append(np.nan)
    t["level_bn_real2024"] = real
    for nm, mem in (("top20", ["q5"]), ("bottom80", ["q1", "q2", "q3", "q4"]), ("all", QS)):
        for y in t.year.unique():
            m = (t.group == nm) & (t.year == y)
            t.loc[m, "level_bn_real2024"] = t[(t.year == y) & t.group.isin(mem)].level_bn_real2024.sum()
    return t


# main reads: each concept ranked by itself (pre-tax PI by equivalized PI, with the 2025 nowcast; DPI, what spending
# is paid from, by equivalized DPI, to 2024). Cross reads (each concept ranked by the other) separate the effect of
# the income concept from that of the ranking.
MAIN_RANK = {"Personal income": "equivalized_pi", "Disposable personal income": "equivalized_dpi"}
PIQ = add_income_aggregates(pidist_levels("Personal income", "equivalized_pi"))
DPIQ = add_income_aggregates(pidist_levels("Disposable personal income", "equivalized_dpi"))
PIQ_X = add_income_aggregates(pidist_levels("Personal income", "equivalized_dpi"))
DPIQ_X = add_income_aggregates(pidist_levels("Disposable personal income", "equivalized_pi"))

INC_WIN = [(2019, 2024), (2019, 2022), (2022, 2024), (2022, 2023), (2023, 2024), (2024, 2025), (2022, 2025),
           (2023, 2025), (2019, 2025)]
INCG = []
for nm, t in (("Personal income", PIQ), ("Disposable personal income", DPIQ), ("Personal income", PIQ_X),
              ("Disposable personal income", DPIQ_X)):
    for g, x in t.groupby("group"):
        x = x.set_index("year")
        for a, b in INC_WIN:
            if a not in x.index or b not in x.index:
                continue
            INCG.append(dict(concept=nm, ranking=x.ranking.iloc[0], group=g, window=f"{a}->{b}", years=b - a,
                             includes_nowcast=b == 2025, g_nominal_pct=100 * (x.loc[b, "level_bn"] /
                                                                              x.loc[a, "level_bn"] - 1),
                             g_real_pct=100 * (x.loc[b, "level_bn_real2024"] / x.loc[a, "level_bn_real2024"] - 1),
                             share_change_pts=100 * (x.loc[b, "share"] - x.loc[a, "share"])))
# rounding: the quintile shares are printed to 0.001 and the 2022 ones sum to 0.999; taking the bottom 80% as one minus
# the top fifth's share (each end deflated by the bottom 80%'s own implicit index) moves its 2022-2025 real growth
pb = PIQ[PIQ.group == "bottom80"].set_index("year")
pq5 = PIQ[PIQ.group == "q5"].set_index("year")
b80_alt = {y: (1 - pq5.loc[y, "share"]) * pb.loc[y, "total_bn"] for y in (2022, 2024)}
b80_alt[2025] = b80_alt[2024] * pb.loc[2025, "level_bn"] / pb.loc[2024, "level_bn"]       # same nowcast growth
defl = {y: pb.loc[y, "level_bn"] / pb.loc[y, "level_bn_real2024"] for y in (2022, 2025)}
INCG.append(dict(concept="Personal income", ranking="equivalized_pi", group="bottom80 (1 - top-20 share)",
                 window="2022->2025", years=3, includes_nowcast=True,
                 g_nominal_pct=100 * (b80_alt[2025] / b80_alt[2022] - 1),
                 g_real_pct=100 * (b80_alt[2025] / defl[2025] / (b80_alt[2022] / defl[2022]) - 1)))
INCG = pd.DataFrame(INCG)


def income_taxes(ranking="equivalized_dpi"):
    """Taxes and personal income by quintile of the ranking (sums of decile shares x totals), 2019-2024, and taxes
    as % of the group's personal income: the summary file has DPI = PI - taxes exactly."""
    rows = []
    for y in range(2019, 2025):
        sel = (PIDIST.year == y) & (PIDIST.metric == "share") & (PIDIST.ranking == ranking)
        tx = PIDIST[sel & (PIDIST.income_concept == "Taxes")].set_index("group").value
        pi_ = PIDIST[sel & (PIDIST.income_concept == "Personal income")].set_index("group").value
        tot = {c: float(PIDIST[(PIDIST.year == y) & (PIDIST.metric == "total") &
                               (PIDIST.income_concept == c)].value.iloc[0])
               for c in ("Taxes", "Personal income", "Disposable personal income")}
        assert abs(tot["Personal income"] - tot["Taxes"] - tot["Disposable personal income"]) < 1e-6
        dec = [f"D{k:02d}" for k in range(1, 11)]
        for g, mem in (("q1", dec[0:2]), ("q2", dec[2:4]), ("q3", dec[4:6]), ("q4", dec[6:8]), ("q5", dec[8:10]),
                       ("bottom80", dec[:8]), ("top20", dec[8:]), ("all", dec)):
            t_bn, p_bn = tx[mem].sum() * tot["Taxes"], pi_[mem].sum() * tot["Personal income"]
            rows.append(dict(year=y, ranking=ranking, group=g, taxes_bn=t_bn, pi_bn=p_bn,
                             taxes_pct_of_pi=100 * t_bn / p_bn))
    return pd.DataFrame(rows)


TAXES = income_taxes()

# joint distribution (BEA-BLS, 2000-2023, deciles of equivalized DPI): saving rates and PCE/DPI by group
JS = JOINT[JOINT.metric == "share"].pivot_table(index=["year", "group"], columns="series", values="value")
JT = JOINT[JOINT.metric == "total"].pivot_table(index="year", columns="series", values="value")
JR = JOINT[JOINT.metric == "saving_rate"].pivot_table(index="year", columns="group", values="value")
JOINT_ROWS = []
for y in range(2019, 2024):
    for g, mem in [(d, [d]) for d in [f"D{k:02d}" for k in range(1, 11)]] + \
                  [("Q1", ["D01", "D02"]), ("Q2", ["D03", "D04"]), ("Q3", ["D05", "D06"]), ("Q4", ["D07", "D08"]),
                   ("Q5", ["D09", "D10"]), ("B80", [f"D{k:02d}" for k in range(1, 9)]), ("T05", ["T05"]),
                   ("T01", ["T01"]), ("B90", [f"D{k:02d}" for k in range(1, 10)]),
                   ("ALL", [f"D{k:02d}" for k in range(1, 11)])]:
        sh = JS.loc[[(y, m) for m in mem]].sum()
        dpi = sh["Disposable Personal Income"] * JT.loc[y, "Disposable Personal Income"]
        pce = sh["Personal Consumption Expenditures"] * JT.loc[y, "Personal Consumption Expenditures"]
        sav = sh["Personal Saving"] * JT.loc[y, "Personal Saving"]
        JOINT_ROWS.append(dict(year=y, group=g, dpi_share=sh["Disposable Personal Income"],
                               pce_share=sh["Personal Consumption Expenditures"], saving_share=sh["Personal Saving"],
                               dpi_bn=dpi, pce_bn=pce, saving_bn=sav, pce_to_dpi=pce / dpi,
                               saving_rate_from_shares=sav / dpi,
                               saving_rate_published=JR.loc[y, g] if g in JR.columns else np.nan))
JOINT_ROWS = pd.DataFrame(JOINT_ROWS)

SR_M = pi_series(35)                      # Table 2.6 line 35, monthly saving rate (% of DPI)
SR_A = pi_series(35, "A")                 # Table 2.1 line 35, annual
SR_A.index = SR_A.index.astype(int)
SAV_M = pi_series(34)
SRM = pd.DataFrame({"date": SR_M.index, "saving_rate_pct": SR_M.values, "saving_bn_saar": SAV_M.loc[SR_M.index].values / 1e3})
SRM = SRM[SRM.date >= "2015-01"]
SRA = pd.DataFrame({"year": SR_A.index.astype(int), "saving_rate_pct_annual": SR_A.values})
SRA = SRA[SRA.year >= 2015]
SRA["saving_rate_pct_mean_of_months"] = [SR_M[[f"{y}-{m:02d}" for m in range(1, 13) if f"{y}-{m:02d}" in SR_M.index]].mean()
                                         for y in SRA.year]

INC = pd.concat([
    pd.concat([PIQ, DPIQ, PIQ_X, DPIQ_X], ignore_index=True).assign(block="income_quintile_levels"),
    INCG.assign(block="income_quintile_growth"),
    TAXES.assign(block="taxes_by_dpi_group", concept="Taxes (summary file; DPI = PI - taxes)"),
    JOINT_ROWS.assign(block="joint_by_dpi_group", concept="BEA-BLS joint distribution (vintage 2026-05)"),
    SRM.assign(block="saving_rate_monthly", concept="NIPA Table 2.6 line 35 (vintage 2026-10-29)"),
    SRA.assign(block="saving_rate_annual", concept="NIPA Table 2.1 line 35 (vintage 2026-10-29)"),
], ignore_index=True)
first = ["block", "concept", "ranking", "group", "year", "date", "window"]
INC = INC[first + [c for c in INC.columns if c not in first]]
write_csv(INC, "direct_income_saving.csv")
print("Section 3 done:", len(INC), "rows")

# %% 6. Section 4: wealth side (DFA by income group), equity gains since 2022Q3, an assumption-driven bound
DFA_CATS = ["Net worth", "Corporate equities and mutual fund shares", "Real estate", "Consumer credit",
            "DC pension entitlements", "Deposits", "Home mortgages", "Household count"]
DFA_DATES = ["2019Q4", "2022Q3", "2025Q2", "2025Q3", "2026Q2"]
dl = DFA[(DFA.measure == "level") & DFA.category.isin(DFA_CATS)].copy()
dl["value"] = dl.value.astype(float)
DFA_LEV = dl.pivot_table(index=["date", "category"], columns="group", values="value")
DFA_LEV["all"] = DFA_LEV[DFA_GROUPS].sum(axis=1)
DFA_LEV["top20"] = DFA_LEV[["pct80to99", "pct99to100"]].sum(axis=1)
DFA_LEV["bottom80"] = DFA_LEV[DFA_GROUPS[:4]].sum(axis=1)
GRP_ALL = DFA_GROUPS + ["top20", "bottom80", "all"]

DFA_ROWS = []
for d in DFA_DATES:
    hh = DFA_LEV.loc[(d, "Household count")]
    for c in DFA_CATS[:-1]:
        lv = DFA_LEV.loc[(d, c)]
        for g in GRP_ALL:
            DFA_ROWS.append(dict(date=d, category=c, group=g, level_bn=lv[g] / 1e3,
                                 share_pct=100 * lv[g] / lv["all"], per_household_k=lv[g] * 1e6 / hh[g] / 1e3,
                                 households_m=hh[g] / 1e6, modelled=d > "2022Q3"))
DFA_ROWS = pd.DataFrame(DFA_ROWS)

# Z.1 (2026:Q2 release): revaluation share of the change in households' and nonprofits' equity-type holdings
Z1 = zipfile.ZipFile(RAW / "fed" / "z1" / "z1_csv_files.zip")
Z1B = pd.read_csv(io.BytesIO(Z1.read("csv/S1M_b.csv"))).set_index("date")
Z1R = pd.read_csv(io.BytesIO(Z1.read("csv/S1M_r.csv"))).set_index("date")
EQ_CODES = ["153064105", "153064205", "153064705", "153064505"]   # corporate equities, mutual funds, hedge, PDF


def z1_reval_share(a, b):
    qa, qb = a[:4] + ":" + a[4:], b[:4] + ":" + b[4:]
    lv = Z1B[[f"LM{c}.Q" for c in EQ_CODES]].apply(pd.to_numeric, errors="coerce").sum(axis=1)   # 'ND' = no data
    rv = Z1R[[f"FR{c}.Q" for c in EQ_CODES]].apply(pd.to_numeric, errors="coerce").sum(axis=1)
    idx = list(Z1R.index)
    reval = rv.iloc[idx.index(qa) + 1: idx.index(qb) + 1].sum()
    return dict(window=f"{a}->{b}", z1_level_start_bn=lv[qa] / 1e3, z1_level_end_bn=lv[qb] / 1e3,
                z1_change_bn=(lv[qb] - lv[qa]) / 1e3, z1_revaluation_bn=reval / 1e3,
                reval_share=reval / (lv[qb] - lv[qa]))


GAIN_WIN = [("2022Q3", "2026Q2"), ("2022Q3", "2025Q2"), ("2019Q4", "2026Q2")]
REVAL = {f"{a}->{b}": z1_reval_share(a, b) for a, b in GAIN_WIN}
REVAL["2024Q2->2026Q2"] = z1_reval_share("2024Q2", "2026Q2")      # alternative for the saving cross-check (T16)

# the timing of the run-up against the CE window (calendar 2022-2025): DFA holdings (all groups) and Z.1 revaluations
EQ_ALL = DFA_LEV.xs("Corporate equities and mutual fund shares", level="category")["all"] / 1e3
RUNUP = []
for a, b in (("2022Q3", "2023Q4"), ("2023Q4", "2024Q4"), ("2024Q4", "2025Q4"), ("2025Q4", "2026Q2")):
    z = z1_reval_share(a, b)
    RUNUP.append(dict(window=f"{a}->{b}", quarters=4 * (int(b[:4]) - int(a[:4])) + int(b[-1]) - int(a[-1]),
                      dfa_change_bn=EQ_ALL[b] - EQ_ALL[a], dfa_change_pct=100 * (EQ_ALL[b] / EQ_ALL[a] - 1),
                      z1_revaluation_bn=z["z1_revaluation_bn"]))
RUNUP = pd.DataFrame(RUNUP)
RUNUP["dfa_change_bn_per_quarter"] = RUNUP.dfa_change_bn / RUNUP.quarters
RUNUP["z1_revaluation_bn_per_quarter"] = RUNUP.z1_revaluation_bn / RUNUP.quarters

# spending shares by DFA income group, for 'share of each group's spending' (two denominators, both scaled to PCE)
S["DFA"] = S.INCPCTLECAT.map(PCT12_TO_DFA)
scf_sh = (S.TOTSPENDNH * S.WGT).groupby(S.DFA).sum()
SPEND_SHARE = {"SCF 2025 non-housing spending, same income ranking as the DFA": scf_sh / scf_sh.sum()}
js23 = JS.loc[2023]["Personal Consumption Expenditures"]
SPEND_SHARE["BEA-BLS joint 2023 PCE shares, deciles of equivalized DPI"] = pd.Series({
    "pct00to20": js23["D01"] + js23["D02"], "pct20to40": js23["D03"] + js23["D04"],
    "pct40to60": js23["D05"] + js23["D06"], "pct60to80": js23["D07"] + js23["D08"],
    "pct80to99": js23["D09"] + js23["D10"] - js23["T01"], "pct99to100": js23["T01"]})
for k in SPEND_SHARE:
    SPEND_SHARE[k] = SPEND_SHARE[k] / SPEND_SHARE[k].sum()

WE = []
GAINS = []
for a, b in GAIN_WIN:
    w = f"{a}->{b}"
    pce_end = pce_quarter(b)
    for base in ("equities (level change)", "equities (revaluation share applied)", "net worth (level change)"):
        cat = "Net worth" if base.startswith("net worth") else "Corporate equities and mutual fund shares"
        dlt = (DFA_LEV.loc[(b, cat)] - DFA_LEV.loc[(a, cat)]) / 1e3
        if "revaluation" in base:
            dlt = dlt * REVAL[w]["reval_share"]
        for g in GRP_ALL:
            GAINS.append(dict(window=w, base=base, group=g, gain_bn=dlt[g],
                              gain_pct=100 * dlt[g] * 1e3 / DFA_LEV.loc[(a, cat)][g],
                              share_of_gain_pct=100 * dlt[g] / dlt["all"]))
        for cwk, cw in CW.items():
            for den, sh in SPEND_SHARE.items():
                cg = {}
                for g in DFA_GROUPS:
                    spend_g = pce_end * sh[g]
                    cg[g] = (cw * dlt[g], spend_g)
                cg["top20"] = tuple(map(sum, zip(cg["pct80to99"], cg["pct99to100"])))
                cg["bottom80"] = tuple(map(sum, zip(*[cg[g] for g in DFA_GROUPS[:4]])))
                cg["all"] = tuple(map(sum, zip(*[cg[g] for g in DFA_GROUPS])))
                for g, (dc, sp) in cg.items():
                    WE.append(dict(window=w, base=base, c_w=cw, c_w_case=cwk, denominator=den, group=g,
                                   wealth_effect_bn_per_year=dc, group_spending_bn=sp,
                                   pct_of_group_spending=100 * dc / sp, pct_of_pce=100 * dc / pce_end,
                                   pce_end_bn_saar=pce_end))
GAINS = pd.DataFrame(GAINS)
WE = pd.DataFrame(WE)
wt = WE.pivot_table(index=["window", "base", "c_w", "denominator"], columns="group", values="pct_of_group_spending")
WE_GAP = (wt["top20"] - wt["bottom80"]).rename("implied_gap_top20_minus_bottom80_pts").reset_index()

# observed counterparts for the same groups: CE top quintile vs bottom 80% (income before taxes), real
ce_gap = GAPS[(GAPS.grouping == "quintile")].set_index("window")
WE_GAP["ce_observed_gap_real_total_pts_2022_2025"] = ce_gap.loc["2022->2025", "gap_real_total_pts"]
WE_GAP["ce_observed_gap_real_consumption_pts_2022_2025"] = ce_gap.loc["2022->2025", "gap_real_consumption_pts"]
WE_GAP["zandi_gap_3yr_pts"] = ce_gap.loc["2022->2025", "zandi_gap_pts"]

# equity concentration: SCF (survey) against the DFA (model after 2022Q3), same income ranking
def scf_conc(df, var, cat_col="INCPCTLECAT"):
    g = df[cat_col].map(PCT12_TO_DFA)
    v = (df[var] * df.WGT).groupby(g).sum()
    return 100 * v / v.sum()


CONC = []
for yr, df, dq in ((2022, SCF22, "2022Q3"), (2025, SCF25, "2025Q3")):
    df = df.copy()
    df["DIRECT_EQ_MF"] = df.STOCKS + df.NMMF
    dfa_sh = 100 * DFA_LEV.loc[(dq, "Corporate equities and mutual fund shares")][DFA_GROUPS] / \
        DFA_LEV.loc[(dq, "Corporate equities and mutual fund shares")]["all"]
    for var, lab in (("DIRECT_EQ_MF", "SCF directly held stocks + non-money-market funds (STOCKS + NMMF)"),
                     ("EQUITY", "SCF all equity held directly or indirectly (EQUITY, incl. retirement accounts)"),
                     ("NETWORTH", "SCF net worth")):
        sh = scf_conc(df, var)
        for g in DFA_GROUPS:
            CONC.append(dict(scf_year=yr, dfa_quarter=dq, concept=lab, group=g, scf_share_pct=sh[g],
                             dfa_equities_share_pct=dfa_sh[g] if var != "NETWORTH" else
                             100 * DFA_LEV.loc[(dq, "Net worth")][g] / DFA_LEV.loc[(dq, "Net worth")]["all"]))
    for var in ("EQUITY", "DEQ", "DIRECT_EQ_MF"):
        tot = (df[var] * df.WGT).sum()
        for top, cats in (("top10", [10, 11, 12]), ("top20", [9, 10, 11, 12]), ("top1", [12])):
            CONC.append(dict(scf_year=yr, concept=f"SCF {var}: share held by the {top} by income", group=top,
                             scf_share_pct=100 * (df[var] * df.WGT)[df.INCPCTLECAT.isin(cats)].sum() / tot))
        # Zandi's '90%' is of the top 10% 'of the income distribution'; the same concepts ranked by wealth
        CONC.append(dict(scf_year=yr, concept=f"SCF {var}: share held by the top10 by WEALTH", group="top10_wealth",
                         scf_share_pct=100 * (df[var] * df.WGT)[df.NWPCTLECAT.isin([10, 11, 12])].sum() / tot))
DFAWLTH = pd.read_csv(TIDY / "dfa_wealth_long.csv")
for dq in ("2022Q3", "2025Q3", "2026Q2"):
    x = DFAWLTH[(DFAWLTH.category == "Corporate equities and mutual fund shares") & (DFAWLTH.measure == "level") &
                (DFAWLTH.date == dq)].set_index("group").value.astype(float)
    CONC.append(dict(dfa_quarter=dq, concept="DFA corporate equities and MF: share held by the top 10% by WEALTH "
                     "(Next9 + RemainingTop1 + TopPt1)", group="top10_wealth",
                     dfa_equities_share_pct=100 * x[["Next9", "RemainingTop1", "TopPt1"]].sum() / x.sum()))
    y = DFA_LEV.loc[(dq, "Corporate equities and mutual fund shares")]
    CONC.append(dict(dfa_quarter=dq, concept="DFA corporate equities and MF: share held by the top 20% by INCOME "
                     "(80-99 + 99-100)", group="top20", dfa_equities_share_pct=100 * y["top20"] / y["all"]))
CONC = pd.DataFrame(CONC)

DFAW = pd.concat([
    DFA_ROWS.assign(block="levels"),
    GAINS.assign(block="gains"),
    pd.DataFrame(REVAL.values()).assign(block="z1_revaluation_share"),
    WE.assign(block="wealth_effect_bound"),
    WE_GAP.assign(block="wealth_effect_gap"),
    CONC.assign(block="concentration_scf_vs_dfa"),
    RUNUP.assign(block="equity_runup_timing", group="all"),
], ignore_index=True)
DFAW["group_label"] = DFAW.group.map(lambda g: DFA_LABEL.get(g, g) if isinstance(g, str) else g)
first = ["block", "date", "window", "category", "base", "group", "group_label"]
DFAW = DFAW[first + [c for c in DFAW.columns if c not in first]]
write_csv(DFAW, "direct_dfa_wealth.csv")
print("Section 4 done:", len(DFAW), "rows")

# %% 7. Section 5 (and the SCF part of section 1): SCF 2025 spending and the windfall question
S["LIQ_FEDS"] = S.LIQ + S.CDS + S.NMMF + S.STOCKS + S.BOND           # FEDS Note fn 15 definition of liquid assets
S["MONTHS_LIQ"] = np.where(S.NORMINC > 0, S.LIQ_FEDS / (S.NORMINC / 12), np.where(S.LIQ_FEDS > 0, np.inf, 0.0))
S["HTM_FEDS"] = S.MONTHS_LIQ < 0.5                                   # < half a month of normal income
S["NETLIQ_KVW"] = S.LIQ + S.NMMF + S.STOCKS + S.BOND - S.CCBAL       # KVW-style net liquid wealth
# illiquid wealth: home equity, other residential real estate net of its debt, net equity in nonresidential real
# estate (NNRESRE), retirement accounts, cash value of life insurance, CDs, savings bonds, other managed assets
S["ILLIQ_KVW"] = S.HOMEEQ + (S.ORESRE - S.RESDBT) + S.NNRESRE + S.RETQLIQ + S.CASHLI + S.CDS + S.SAVBND + S.OTHMA
S["HTM_KVW"] = np.where(S.NETLIQ_KVW <= S.INCOME / 24,
                        np.where(S.ILLIQ_KVW > 0, "wealthy hand-to-mouth", "poor hand-to-mouth"),
                        "not hand-to-mouth")
S["LIQ_BIN"] = pd.cut(np.minimum(S.MONTHS_LIQ, 1e12), [-np.inf, 0.5, 2, 6, 24, np.inf], right=False,
                      labels=["<0.5 month (hand-to-mouth)", "0.5-2 months", "2-6 months", "6-24 months",
                              "24+ months"]).astype(str)
S["Q_NINC"] = ((S.DEC_NINC + 1) // 2).astype(int)
S["Q_INC"] = ((S.DEC_INC + 1) // 2).astype(int)
S["HTM_X_QNINC"] = np.where(S.HTM_FEDS, "HtM", "not HtM") + ", usual-income Q" + S.Q_NINC.astype(str)
S["WSAVED_LAB"] = S.WSAVED.map({1: "spending exceeded income", 2: "spending equaled income",
                                3: "spending below income"}).fillna("n/a")
S["SPEND_PLUS_DEBT"] = S.MPSPEND + S.MPDEBT
S["WINDFALL"] = S.NORMINC / 12
# families with zero or negative usual income have no months-of-income ratio: those holding any account (the extract
# sets LIQ to 1 for zero balances) are binned at 24+, which keeps the '<0.5 month' bin identical to the hand-to-mouth
# group (they are not hand-to-mouth under the note's definition either)
NONPOS_INC_BINNED_24 = S.WGT[(S.NORMINC <= 0) & (S.LIQ_FEDS > 0)].sum() / 1e6
assert ((S.LIQ_BIN == "<0.5 month (hand-to-mouth)") == S.HTM_FEDS).all()
# the top 1% of usual income: distinct families with at least one implicate in it, and family-equivalents (records / 5)
TOP1_FAMILIES = S.YY1[S.NINCPCTLECAT == 12].nunique()
TOP1_RECORDS_OVER_5 = (S.NINCPCTLECAT == 12).sum() / 5
print(f"SCF 2025: families with usual income <= 0 binned at 24+ months: {NONPOS_INC_BINNED_24:.4f}m; top-1% usual-"
      f"income group: {TOP1_FAMILIES} distinct families, {TOP1_RECORDS_OVER_5:.0f} family-equivalents")

GROUPINGS = {   # name: (column, label function, ranking text)
    "all": (None, None, "all families"),
    "usual income, 12 groups": ("NINCPCTLECAT", PCT12_LABEL.get, "usual income NORMINC (publisher's ranking)"),
    "usual income, deciles": ("DEC_NINC", lambda k: f"D{k}", "usual income NORMINC"),
    "usual income, 6 groups": ("NINCCAT", CAT6_LABEL.get, "usual income NORMINC (Bulletin groups)"),
    "income 2024, 12 groups": ("INCPCTLECAT", PCT12_LABEL.get, "family income in 2024 (INCOME)"),
    "income 2024, deciles": ("DEC_INC", lambda k: f"D{k}", "family income in 2024 (INCOME)"),
    "income 2024, 6 groups": ("INCCAT", CAT6_LABEL.get, "family income in 2024 (INCOME)"),
    "income 2024, DFA groups": ("DFA", DFA_LABEL.get, "family income in 2024 (the DFA's income groups)"),
    "net worth, 12 groups": ("NWPCTLECAT", PCT12_LABEL.get, "net worth (publisher's wealth ranking)"),
    "net worth, deciles": ("DEC_NW", lambda k: f"D{k}", "net worth"),
    "hand-to-mouth (FEDS Note definition)": ("HTM_FEDS", lambda b: "hand-to-mouth" if b else "not hand-to-mouth",
                                             "liquid assets < 1/2 month of usual income"),
    "hand-to-mouth (KVW-style, poor/wealthy)": ("HTM_KVW", str, "net liquid wealth <= 1/2 month of 2024 income; "
                                                "wealthy if illiquid wealth > 0"),
    "liquidity, months of usual income": ("LIQ_BIN", str, "liquid assets / (usual income / 12)"),
    "hand-to-mouth x usual-income quintile": ("HTM_X_QNINC", str, "FEDS hand-to-mouth status within quintiles"),
    "spending vs income last year (WSAVED)": ("WSAVED_LAB", str, "self-reported, past 12 months"),
}
SORT = {"<0.5 month (hand-to-mouth)": 0, "0.5-2 months": 1, "2-6 months": 2, "6-24 months": 3, "24+ months": 4,
        "poor hand-to-mouth": 0, "wealthy hand-to-mouth": 1, "not hand-to-mouth": 2, "hand-to-mouth": 0,
        "spending exceeded income": 0, "spending equaled income": 1, "spending below income": 2}

fam_codes, fam_index = np.unique(S.YY1.values, return_inverse=True)
W0 = S.WGT.values.astype(float)


def group_codes(col):
    if col is None:
        return np.zeros(len(S), int), ["all"]
    keys = S[col]
    uniq = sorted(keys.unique(), key=lambda k: (SORT.get(k, 99), k) if isinstance(k, str) else (0, k))
    assert not keys.isna().any(), col
    m = {k: i for i, k in enumerate(uniq)}
    return keys.map(m).values.astype(int), uniq


def grouped_means(code, k, w, vals):
    den = np.bincount(code, weights=w, minlength=k)
    return {v: np.bincount(code, weights=w * x, minlength=k) / den for v, x in vals.items()}, den


VALS = {"spend": S.MPSPEND.values, "save": S.MPSAVE.values, "debt": S.MPDEBT.values,
        "spend_plus_debt": S.SPEND_PLUS_DEBT.values, "spend_x_inc": S.MPSPEND.values * S.NORMINC.values,
        "inc": S.NORMINC.values, "zero_spend": (S.MPSPEND.values == 0).astype(float),
        "all_spend": (S.MPSPEND.values == 100).astype(float), "windfall": S.WINDFALL.values}
rng = np.random.default_rng(SEED)
BOOT_W = [W0 * rng.multinomial(len(fam_codes), np.full(len(fam_codes), 1 / len(fam_codes)))[fam_index]
          for _ in tqdm(range(N_BOOT), desc="family bootstrap weights")]

WF = []
BOOTS = {}
for gname, (col, labf, rk) in GROUPINGS.items():
    code, uniq = group_codes(col)
    k = len(uniq)
    est, den = grouped_means(code, k, W0, VALS)
    bs = np.array([grouped_means(code, k, wb, {"spend": VALS["spend"]})[0]["spend"] for wb in BOOT_W])
    BOOTS[gname] = (uniq, bs)
    for i, key in enumerate(uniq):
        lab = "all families" if col is None else labf(key)
        WF.append(dict(grouping=gname, ranking=rk, group=lab, group_key=str(key), families_m=den[i] / 1e6,
                       share_of_families_pct=100 * den[i] / W0.sum(), spend_pct=est["spend"][i],
                       save_pct=est["save"][i], debt_pct=est["debt"][i],
                       spend_plus_debt_pct=est["spend_plus_debt"][i],
                       spend_income_weighted_pct=est["spend_x_inc"][i] / est["inc"][i],
                       share_spend_none_pct=100 * est["zero_spend"][i], share_spend_all_pct=100 * est["all_spend"][i],
                       mean_windfall_usd=est["windfall"][i], se_spend_boot=bs[:, i].std(ddof=1)))
WF = pd.DataFrame(WF)

# publisher figures (FEDS Note accessible tables) beside the extract's
pub_inc = FEDS["by_normal_income"].set_index("pct12")
pub_nw = FEDS["by_wealth"].set_index("pct12")
WF["publisher_spend_pct"] = np.nan
WF["publisher_save_pct"] = np.nan
WF["publisher_debt_pct"] = np.nan
for gname, pub in (("usual income, 12 groups", pub_inc), ("net worth, 12 groups", pub_nw)):
    m = WF.grouping == gname
    keys = WF.loc[m, "group_key"].astype(float).astype(int)
    WF.loc[m, "publisher_spend_pct"] = keys.map(pub.spend).values
    WF.loc[m, "publisher_save_pct"] = keys.map(pub.save).values
    WF.loc[m, "publisher_debt_pct"] = keys.map(pub.debt).values
ov = FEDS["overall"].iloc[0]
m = WF.grouping == "all"
WF.loc[m, ["publisher_spend_pct", "publisher_save_pct", "publisher_debt_pct"]] = [ov["Spend"], ov["Save"],
                                                                                   ov["Pay Debt"]]

# regression-adjusted means by hand-to-mouth status, the FEDS Note's Figure 4 recipe (WLS on log usual income)
X = np.column_stack([np.ones(len(S)), S.HTM_FEDS.astype(float), np.log(np.maximum(S.NORMINC, 1.0))])
sw = np.sqrt(W0)
beta = np.linalg.lstsq(X * sw[:, None], S.MPSPEND.values * sw, rcond=None)[0]
lbar = wmean(X[:, 2], W0)
HTM_ADJ = {"not hand-to-mouth": beta[0] + beta[2] * lbar, "hand-to-mouth": beta[0] + beta[1] + beta[2] * lbar}
pub_htm = FEDS["htm"].set_index(FEDS["htm"].columns[0]).iloc[:, 0]
for lab, v in HTM_ADJ.items():
    WF.loc[len(WF)] = dict(grouping="hand-to-mouth, regression-adjusted (FEDS Note Fig. 4 recipe)",
                           ranking="WLS of MPSPEND on HtM and log usual income, at the mean log income",
                           group=lab, group_key=lab, spend_pct=v,
                           publisher_spend_pct=pub_htm["Hand-to-Mouth" if lab == "hand-to-mouth" else
                                                       "Not Hand-to-Mouth"])

# the gradient the post assumes (spend share relative to the bottom decile) against the SCF
GRAD = []
for gname, top_keys, bot_keys in (("usual income, deciles", [10], [1]), ("income 2024, deciles", [10], [1]),
                                  ("usual income, 12 groups", [12], [1]), ("income 2024, 12 groups", [12], [1])):
    uniq, bs = BOOTS[gname]
    x = WF[WF.grouping == gname].reset_index(drop=True)
    it = [uniq.index(k) for k in top_keys][0]
    ib = [uniq.index(k) for k in bot_keys][0]
    r = x.spend_pct[it] / x.spend_pct[ib]
    rb = bs[:, it] / bs[:, ib]
    GRAD.append(dict(grouping=gname, top=x.group[it], bottom=x.group[ib], spend_top=x.spend_pct[it],
                     spend_bottom=x.spend_pct[ib], ratio_spend=r, ratio_spend_lo95=np.quantile(rb, 0.025),
                     ratio_spend_hi95=np.quantile(rb, 0.975),
                     ratio_spend_plus_debt=x.spend_plus_debt_pct[it] / x.spend_plus_debt_pct[ib],
                     ratio_income_weighted=x.spend_income_weighted_pct[it] / x.spend_income_weighted_pct[ib],
                     post_ratio_lo=POST_MPC_TOP[0] / POST_MPC_BOTTOM, post_ratio_hi=POST_MPC_TOP[1] / POST_MPC_BOTTOM))
GRAD = pd.DataFrame(GRAD)
WFALL = pd.concat([WF.assign(block="windfall"), GRAD.assign(block="gradient_vs_post")], ignore_index=True)
first = ["block", "grouping", "ranking", "group"]
WFALL = WFALL[first + [c for c in WFALL.columns if c not in first]]
write_csv(WFALL, "direct_scf2025_windfall.csv")

# SCF 2025 spending by group (non-housing spending, and with renters' rent), with the Bulletin's Box 1 figures
SP = []
SPEND_GROUPINGS = ["all", "income 2024, deciles", "income 2024, 6 groups", "income 2024, 12 groups",
                   "income 2024, DFA groups", "usual income, 6 groups", "usual income, deciles",
                   "net worth, 6 groups"]
S["NWCAT6"] = pd.cut(S.NWPCTLECAT, [0, 2, 4, 6, 8, 9, 12], labels=[1, 2, 3, 4, 5, 6]).astype(int)
GROUPINGS["net worth, 6 groups"] = ("NWCAT6", CAT6_LABEL.get, "net worth (Bulletin groups)")
for gname in SPEND_GROUPINGS:
    col, labf, rk = GROUPINGS[gname]
    code, uniq = group_codes(col)
    for i, key in enumerate(uniq):
        x = S[code == i]
        w = x.WGT.values
        agg = (x.TOTSPENDNH * x.WGT).sum()
        SP.append(dict(grouping=gname, ranking=rk, group="all families" if col is None else labf(key),
                       group_key=str(key), families_m=w.sum() / 1e6,
                       mean_totspendnh=wmean(x.TOTSPENDNH, w), median_totspendnh=wquantile(x.TOTSPENDNH, w, 0.5),
                       aggregate_totspendnh_bn=agg / 1e9,
                       share_of_aggregate_pct=100 * agg / (S.TOTSPENDNH * S.WGT).sum(),
                       mean_spend_plus_rent=wmean(x.SPEND_RENT, w),
                       share_spend_plus_rent_pct=100 * (x.SPEND_RENT * x.WGT).sum() / (S.SPEND_RENT * S.WGT).sum(),
                       mean_income_2024=wmean(x.INCOME, w), mean_usual_income=wmean(x.NORMINC, w),
                       spend_to_income_aggregate=agg / (x.INCOME * x.WGT).sum(),
                       mean_vacation=wmean(x.VACATION, w), mean_food_home=wmean(x.FOODHOME, w),
                       mean_food_away_incl_delivery=wmean(x.FOODAWAY + x.FOODDELV, w)))
SP = pd.DataFrame(SP)
BULLETIN = {("all", "all families"): dict(mean=48700, median=33700, share=None),
            ("usual income, 6 groups", "0-20"): dict(mean=17600, share=7.2),
            ("usual income, 6 groups", "80-90"): dict(mean=68700),
            ("usual income, 6 groups", "90-100"): dict(mean=138800, share=28.5),
            ("net worth, 6 groups", "0-20"): dict(mean=23400), ("net worth, 6 groups", "80-90"): dict(mean=68800),
            ("net worth, 6 groups", "90-100"): dict(mean=136000, share=27.9)}
SP["bulletin_mean"] = [BULLETIN.get((g, l), {}).get("mean") for g, l in zip(SP.grouping, SP.group)]
SP["bulletin_median"] = [BULLETIN.get((g, l), {}).get("median") for g, l in zip(SP.grouping, SP.group)]
SP["bulletin_share_pct"] = [BULLETIN.get((g, l), {}).get("share") for g, l in zip(SP.grouping, SP.group)]
write_csv(SP, "direct_scf2025_spending.csv")
print("Section 5 done:", len(WFALL), "windfall rows,", len(SP), "spending rows")

# %% 8. Section 6: evidence table (numbers pulled from the outputs above)
def gap(kind, window, col="gap_real_total_pts"):
    return float(GAPS[(GAPS.grouping == kind) & (GAPS.window == window)][col].iloc[0])


def incg(concept, group, window, col="g_real_pct", ranking=None):
    """growth of an income concept by group; by default each concept ranked by itself (MAIN_RANK)"""
    rk = ranking or MAIN_RANK[concept]
    x = INCG[(INCG.concept == concept) & (INCG.ranking == rk) & (INCG.group == group) & (INCG.window == window)]
    assert len(x) == 1, (concept, rk, group, window)
    return float(x[col].iloc[0])


def taxes(group, year, col="taxes_pct_of_pi"):
    return float(TAXES[(TAXES.group == group) & (TAXES.year == year)][col].iloc[0])


def jrow(group, year, col="saving_rate_published"):
    return float(JOINT_ROWS[(JOINT_ROWS.group == group) & (JOINT_ROWS.year == year)][col].iloc[0])


def weg(window, cw, den_key, base="equities (revaluation share applied)"):
    x = WE_GAP[(WE_GAP.window == window) & (WE_GAP.c_w == cw) & (WE_GAP.base == base) &
               WE_GAP.denominator.str.startswith(den_key)]
    return float(x.implied_gap_top20_minus_bottom80_pts.iloc[0])


def wfv(grouping, group, col="spend_pct"):
    return float(WF[(WF.grouping == grouping) & (WF.group == group)][col].iloc[0])


z22, z23 = ZSH.iloc[0], ZSH.iloc[1]
gq = GAPS.set_index(["grouping", "window"])
gains_26 = GAINS[(GAINS.window == "2022Q3->2026Q2") & (GAINS.base == "equities (level change)")].set_index("group")
grad = GRAD.set_index("grouping")
sr_m = SR_M
SAV_FIN_SHARE = 100 * -(SAV_M["2026-09"] - SAV_M["2026-03"]) / (PCE_M["2026-09"] - PCE_M["2026-03"])
CE_SE_LEVEL = TS[(TS.source == CEQ) & (TS.group == "top20") & TS.year.between(2019, 2025)].se_pct
PCE_2025_TN = PCE_A["2025"] / 1e6                     # calendar 2025, NIPA Table 2.1 line 29 (vintage 2026-10-29)
SCF_AGG_TN = (S.TOTSPENDNH * S.WGT).sum() / 1e12      # SCF 2025 non-housing spending, past 12 months
RUN_2026H1 = RUNUP.set_index("window").loc["2025Q4->2026Q2"]
DPI_T, DPI_B = (incg("Disposable personal income", g, "2022->2024") for g in ("top20", "bottom80"))
DPI_T3, DPI_B3 = (incg("Disposable personal income", g, "2023->2024") for g in ("top20", "bottom80"))
DPI_GAP_2224 = DPI_T - DPI_B
PI_B80_ALT = incg("Personal income", "bottom80 (1 - top-20 share)", "2022->2025")
CE_SE_TXT = f"{gap('quintile', '2022->2025', 'se_gap_pts'):.1f}"
EVID = [
    dict(source="CE Table 1101/1110 (BLS), top shares of total expenditures",
         ranking="income before taxes, consumer units, unequivalized", years="2014-2025 (deciles), 2019-2025 (quintiles)",
         shows=f"Top 20% share {ts(CEQ, 'top20', 2019):.1f}% (2019), {ts(CEQ, 'top20', 2022):.1f}% (2022), "
               f"{ts(CEQ, 'top20', 2023):.1f}% (2023), {ts(CEQ, 'top20', 2025):.1f}% (2025), approx. SE "
               f"{CE_SE_LEVEL.min():.2f}-{CE_SE_LEVEL.max():.2f}; Zandi's split implies "
               f"{z22.zandi_share_2025_nominal_pct:.1f}% by 2025 from 2022 ({z22.zandi_minus_observed_in_ses:.1f} SEs "
               f"of the change above the observed share; {z23.zandi_share_2025_nominal_pct:.1f}% from 2023, "
               f"{z23.zandi_minus_observed_in_ses:.1f} SEs). Top 10% {ts(CED, 'top10', 2022):.1f}% -> "
               f"{ts(CED, 'top10', 2025):.1f}%.",
         consistent="no",
         caveat="CE under-covers the very top (no oversample; nonresponse and under-reporting rise with income); "
                "2025 collected through the Oct-Nov 2025 funding lapse (reweighted, Fay's BRR SEs)."),
    dict(source="CE (BLS), real growth by group, ISPCEPX-deflated",
         ranking="income before taxes, CU, unequivalized", years="2022-2025, 2023-2025, 2024-2025",
         shows=f"Real aggregate spending 2022->2025: top 20% "
               f"+{gq.loc[('quintile', '2022->2025'), 'top_real_total']:.1f}%, "
               f"bottom 80% +{gq.loc[('quintile', '2022->2025'), 'bottom_real_total']:.1f}% "
               f"(gap {gap('quintile', '2022->2025'):+.1f} pts, approx. SE {CE_SE_TXT}; "
               f"Zandi {gap('quintile', '2022->2025', 'zandi_gap_pts'):+.1f}). 2023->2025 gap "
               f"{gap('quintile', '2023->2025'):+.1f} (SE {gap('quintile', '2023->2025', 'se_gap_pts'):.1f}; Zandi "
               f"{gap('quintile', '2023->2025', 'zandi_gap_pts'):+.1f}). Excluding pensions, Social Security and cash "
               f"contributions: {gap('quintile', '2022->2025', 'gap_real_consumption_pts'):+.1f} and "
               f"{gap('quintile', '2023->2025', 'gap_real_consumption_pts'):+.1f}. Top 10% vs bottom 90%, 2022->2025: "
               f"{gap('decile', '2022->2025'):+.1f} (SE {gap('decile', '2022->2025', 'se_gap_pts'):.1f}). The latest "
               f"year alone, 2024->2025: {gap('quintile', '2024->2025'):+.1f} (SE "
               f"{gap('quintile', '2024->2025', 'se_gap_pts'):.1f}) against Zandi's "
               f"{gap('quintile', '2024->2025', 'zandi_gap_pts'):+.1f}, which fits either story.",
         consistent="no",
         caveat="Same coverage caveat. The case against the split rests on the multi-year windows, and the equity "
                "run-up was fastest after the CE window closed (DFA equity holdings "
                f"+${RUN_2026H1.dfa_change_bn / 1e3:.1f}tn in 2026H1). ISPCEPX is a PCE-scope deflator by deciles of "
                "equivalized DPI, not CE income groups, with imputed 2024 weights; 2025 deflated with aggregate PCE "
                "prices (no group index yet)."),
    dict(source="BLS distributional PCE, top shares of PCE",
         ranking="equivalized total PCE (spending), CU-weighted", years="2000-2023",
         shows=f"Top 20% {ts(DP2, 'top20', 2019):.1f}% (2019), {ts(DP2, 'top20', 2022):.1f}% (2022), "
               f"{ts(DP2, 'top20', 2023):.1f}% (2023); top 10% {ts(DP1, 'top10', 2022):.1f}% -> {ts(DP1, 'top10', 2023):.1f}%.",
         consistent="can't tell",
         caveat="Ends in 2023, the start of Zandi's window; ranked by spending, so the top is the top spenders, not "
                "the top earners; 2022->2023 moved against a K."),
    dict(source="BEA-BLS joint distribution, PCE shares",
         ranking="equivalized disposable personal income, households", years="2000-2023",
         shows=f"Top 20% by DPI {ts(JNT, 'top20', 2019):.1f}% of PCE (2019), {ts(JNT, 'top20', 2022):.1f}% (2022), "
               f"{ts(JNT, 'top20', 2023):.1f}% (2023); top 10% {ts(JNT, 'top10', 2023):.1f}%.",
         consistent="can't tell",
         caveat="Ends in 2023; research-stage statistics; PCE side allocated with CE-based shares, which put only "
                f"{ts(JNT, 'top1', 2023):.1f}% of PCE with the top 1% by DPI."),
    dict(source="BEA-BLS joint distribution, saving rates (top)",
         ranking="equivalized DPI", years="2019-2023",
         shows=f"Top decile saving rate {100 * jrow('D10', 2019):.1f}% (2019), {100 * jrow('D10', 2021):.1f}% (2021), "
               f"{100 * jrow('D10', 2022):.1f}% (2022), {100 * jrow('D10', 2023):.1f}% (2023): not below 2019 by 2023.",
         consistent="can't tell",
         caveat="Ends in 2023, before most of Zandi's window and before the 2025-26 equity run-up, so it cannot test "
                "his claim that the rich now save less: it shows only that the top's saving rate had not fallen by "
                "2023."),
    dict(source="BEA-BLS joint distribution, saving rates (bottom 80%)",
         ranking="equivalized DPI", years="2019-2023",
         shows=f"Bottom 80% saving rate {100 * jrow('B80', 2019, 'saving_rate_from_shares'):.1f}% (2019), "
               f"{100 * jrow('B80', 2022, 'saving_rate_from_shares'):.1f}% (2022), "
               f"{100 * jrow('B80', 2023, 'saving_rate_from_shares'):.1f}% (2023): spending further above income by "
               "2022, slightly less so in 2023.",
         consistent="can't tell",
         caveat="Ends in 2023, before the drawdown Zandi describes (2025-26), and the 2019-2023 fall happened by 2022, "
                "then partly reversed. Negative rates at the bottom are partly a construction effect (CE-based PCE "
                "allocated to CPS-based DPI groups); the change, not the level, is the signal."),
    dict(source="BEA distribution of personal income (2025 experimental nowcast)",
         ranking="equivalized personal income, households (2025: ranking not stated)", years="2019-2025",
         shows=f"Real PI 2022->2025: top 20% +{incg('Personal income', 'top20', '2022->2025'):.1f}%, bottom 80% "
               f"+{incg('Personal income', 'bottom80', '2022->2025'):.1f}%; nominal 2024->2025 nowcast: top 20% "
               f"+{incg('Personal income', 'top20', '2024->2025', 'g_nominal_pct'):.1f}%, bottom 80% "
               f"+{incg('Personal income', 'bottom80', '2024->2025', 'g_nominal_pct'):.1f}%.",
         consistent="no",
         caveat="Income before taxes, including in-kind Medicare and Medicaid; spending is paid from disposable income "
                "(next row). 2024 provisional, 2025 an experimental nowcast; shares rounded to 0.001 (bottom 80% taken "
                f"as one minus the top fifth's share: +{PI_B80_ALT:.1f}%)."),
    dict(source="BEA distribution of personal income: disposable personal income (DPI)",
         ranking="equivalized disposable personal income, households", years="2019-2024",
         shows=f"Real DPI 2022->2024: top 20% +{DPI_T:.1f}%, bottom 80% +{DPI_B:.1f}% (gap {DPI_GAP_2224:+.1f} pts), "
               f"all of it in 2022->2023; 2023->2024 top 20% +{DPI_T3:.1f}%, bottom 80% +{DPI_B3:.1f}%. Taxes took "
               f"{taxes('top20', 2022):.1f}% of the top fifth's personal income in 2022 and {taxes('top20', 2024):.1f}% "
               f"in 2024 (bottom 80%: {taxes('bottom80', 2022):.1f}% and {taxes('bottom80', 2024):.1f}%).",
         consistent="can't tell",
         caveat="The income spending is paid from. The tilt to the top came from taxes falling back from a 2022 peak "
                "that was heaviest at the top (DPI ranked by personal income shows it too), is "
                f"{DPI_GAP_2224 / gap('quintile', '2023->2025', 'zandi_gap_pts'):.0%} of Zandi's two-year "
                f"{gap('quintile', '2023->2025', 'zandi_gap_pts'):.1f} points, and stopped in 2024; the series ends in "
                "2024 (provisional), before most of his window."),
    dict(source="NIPA personal saving rate (Table 2.6)",
         ranking="aggregate (no distribution)", years="2019-01 to 2026-09",
         shows=f"{SR_A[2019]:.1f}% (2019), {SR_A[2022]:.1f}% (2022), {SR_A[2024]:.1f}% (2024), {SR_A[2025]:.1f}% "
               f"(2025), {sr_m['2026-09']:.1f}% (Sep 2026); the fall in saving from Mar to Sep 2026 equals "
               f"{SAV_FIN_SHARE:.0f}% of the rise in PCE over those six months (as in NOTES_sectors.md).",
         consistent="can't tell",
         caveat="Who is drawing down saving is not observed after 2023: Zandi's two stories (the rich need to save "
                "less; the lower middle draws down) both fit an aggregate decline."),
    dict(source="SCF 2025 (Fed), total non-housing spending",
         ranking="family income in 2024 (also usual income)", years="2025 survey (spending over the past 12 months)",
         shows=f"Top 10% by income {ts(SCF_MAIN, 'top10', 2025):.1f}% of non-housing spending, top 20% "
               f"{ts(SCF_MAIN, 'top20', 2025):.1f}%, top 1% {ts(SCF_MAIN, 'top1', 2025):.1f}%.",
         consistent="can't tell",
         caveat="One cross-section, first time asked: no trend. Scope excludes housing, loan payments and "
                f"retirement contributions; one summary question; aggregate ${SCF_AGG_TN:.1f}tn against "
                f"${PCE_2025_TN:.2f}tn of PCE in calendar 2025 (NIPA Table 2.1)."),
    dict(source="SCF 2025 (Fed), one-month windfall question",
         ranking="usual income (publisher), 2024 income, liquidity", years="2025 survey",
         shows=f"Share spent: bottom decile {wfv('usual income, deciles', 'D1'):.1f}%, top decile "
               f"{wfv('usual income, deciles', 'D10'):.1f}%, top 1% {wfv('usual income, 12 groups', '99-100'):.1f}%; "
               f"top/bottom decile ratio {grad.loc['usual income, deciles', 'ratio_spend']:.2f} "
               f"(95% {grad.loc['usual income, deciles', 'ratio_spend_lo95']:.2f}-"
               f"{grad.loc['usual income, deciles', 'ratio_spend_hi95']:.2f}) against the post's "
               f"{POST_MPC_TOP[0]:.2f}-{POST_MPC_TOP[1]:.2f}.",
         consistent="can't tell",
         caveat="A hypothetical, one-off windfall of a month's income, stated intention, 12-month horizon: bears on "
                "the ordering of the post's MPC gradient (who spends more of a windfall), not on the level or the "
                "exact slope of an MPC out of a permanent flow."),
    dict(source="Fed DFA, corporate equities and mutual fund shares",
         ranking="SCF family income percentiles (unequivalized), households", years="2019Q4-2026Q2",
         shows=f"Equity holdings rose ${gains_26.loc['all', 'gain_bn'] / 1e3:.1f}tn from 2022Q3 to 2026Q2; the "
               f"top 20% by income got {gains_26.loc['top20', 'share_of_gain_pct']:.0f}% of it "
               f"(80-99: {gains_26.loc['pct80to99', 'share_of_gain_pct']:.0f}%, 99-100: "
               f"{gains_26.loc['pct99to100', 'share_of_gain_pct']:.0f}%).",
         consistent="yes",
         caveat="Wealth, not spending. After 2022Q3 the group split is the DFA's model extrapolation (SCF 2025 not yet "
                "in); for directly held stocks and funds SCF 2025 gives the top 20% a similar share."),
    dict(source="Wealth-effect bound (assumption: 2-5 cents per dollar per year, the post's range)",
         ranking="DFA income groups; SCF 2025 or BEA-BLS 2023 spending shares as denominators",
         years="2022Q3-2025Q2, 2022Q3-2026Q2",
         shows=f"Implied top 20% minus bottom 80% spending gap from equity revaluation gains, SCF denominators: "
               f"{weg('2022Q3->2025Q2', 0.02, 'SCF'):.1f} to {weg('2022Q3->2025Q2', 0.05, 'SCF'):.1f} pts by 2025Q2 "
               f"({weg('2022Q3->2025Q2', 0.035, 'SCF'):.1f} at 3.5 cents), {weg('2022Q3->2026Q2', 0.02, 'SCF'):.1f} to "
               f"{weg('2022Q3->2026Q2', 0.05, 'SCF'):.1f} by 2026Q2; BEA-BLS denominators: "
               f"{weg('2022Q3->2025Q2', 0.02, 'BEA'):.1f} to {weg('2022Q3->2025Q2', 0.05, 'BEA'):.1f} and "
               f"{weg('2022Q3->2026Q2', 0.02, 'BEA'):.1f} to {weg('2022Q3->2026Q2', 0.05, 'BEA'):.1f}. CE shows "
               f"{gap('quintile', '2022->2025'):+.1f} ({gap('quintile', '2022->2025', 'gap_real_consumption_pts'):+.1f} "
               "excluding pensions and contributions).",
         consistent="can't tell",
         caveat="An assumption-driven bound, not a measurement: uniform propensity across groups (likely too high for "
                "the top 1%), no lags, gains include 2026 and only revaluations count. The post's footnote 31 and Fig 0 "
                f"give {POST_CW_FIG0[0]:.0f}-{POST_CW_FIG0[1]:.0f} cents, its body text {POST_CW_BODY[0]:.0f}-"
                f"{POST_CW_BODY[1]:.0f}; Figs 8-10 use {100 * POST_CW_FIGS:.1f}."),
    dict(source="Fingerprint test (sibling unit, NOTES_fingerprint.md)",
         ranking="dPCE (spending) and CE (income) category market shares",
         years="2022-09 to 2026-09 (two-, three- and four-year windows)",
         shows=("Without the care lines, the dPCE source (spending-ranked) reads at its calm-years reference in every "
                "window (within 2 points, real); the CE source (income-ranked) reads above its reference in most "
                "windows in real terms (three years: +1.8 like for like, -0.7 to +6.7 by theta year, where Zandi's "
                "split adds 12.5; two and four years: +5 to +10 and +14 to +15, where it adds 8.2 and 17.0), but "
                "below it in nominal terms. With the care lines in, the dPCE source reads below its reference, "
                "because it gives health care to its recipients."),
         consistent="can't tell",
         caveat=("Can neither confirm nor rule out a K of Zandi's size: where group totals are known, the CE "
                 "source's three-year error has a standard deviation of 47 points (Zandi's gap: 12.5), and it read "
                 "+97 for the CE's own +8.7 in 2020-2023; the calm-years reference rests on 1-3 non-overlapping "
                 "windows; the category mix cannot tell a care boom from a K.")),
    dict(source="Moody's estimates (press reports: top 10% about half of spending)",
         ranking="not published", years="2025",
         shows="Not used: method and data are not public, so the figure cannot be checked or put on a footing.",
         consistent="can't tell", caveat="Not data in the sense used here."),
]
EVID = pd.DataFrame(EVID).rename(columns={"shows": "what_it_shows_top_vs_rest",
                                          "consistent": "consistent_with_zandi_split"})
write_csv(EVID, "direct_evidence_table.csv")
print("Section 6 done:", len(EVID), "evidence rows")

# %% 9. Charts (dataviz skill: reference palette validated for these slots, light surface, hairline solid grid,
#    legend for two or more series plus selective direct labels, text in ink tokens, no dual axes; 200 dpi PNG)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "axes.edgecolor": AXIS, "axes.linewidth": 0.8,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
                     "axes.facecolor": SURF, "figure.facecolor": SURF, "savefig.facecolor": SURF,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "grid.linestyle": "-",
                     "legend.frameon": False, "legend.fontsize": 8.5, "axes.titlesize": 10,
                     "axes.titleweight": "bold", "axes.titlecolor": INK})


def style_axes(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    ax.set_axisbelow(True)


# --- figure 1: top shares by source --------------------------------------------------------------------------
SRC = [("CE, income before taxes (CU)", BLUE, {"top10": CED, "top20": "CE Table 1110 (deciles d09+d10)"}),
       ("BLS dPCE, equivalized spending", ORANGE, {"top10": DP1, "top20": DP2}),
       ("BEA-BLS joint, equivalized DPI", AQUA, {"top10": JNT, "top20": JNT})]
fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.4), gridspec_kw=dict(wspace=0.16))
for ax, grp, ttl in zip(axes, ("top10", "top20"), ("Top 10% share of spending, %", "Top 20% share of spending, %")):
    style_axes(ax)
    ax.axvspan(2022.5, 2025.6, color=GRID, alpha=0.55, lw=0, zorder=0)
    for lab, col, srcs in SRC:
        x = TS[(TS.source == srcs[grp]) & (TS.group == grp)].sort_values("year")
        if srcs[grp] == JNT:
            x = x[x.year >= 2004]          # BEA's page: the joint statistics are "provided for 2004-2023"
        ax.plot(x.year, x.share_pct, color=col, lw=1.8, solid_capstyle="round", zorder=3, label=lab)
        ax.scatter(x.year.iloc[-1], x.share_pct.iloc[-1], s=30, color=col, edgecolor=SURF, linewidth=1.4, zorder=4)
        ax.annotate(f"{x.share_pct.iloc[-1]:.1f}", (x.year.iloc[-1], x.share_pct.iloc[-1]), xytext=(6, 0),
                    textcoords="offset points", fontsize=7.8, color=INK2, va="center")
    v = ts(SCF_MAIN, grp, 2025)
    ax.scatter([2025], [v], s=46, marker="D", color=YELLOW, edgecolor=SURF, linewidth=1.4, zorder=5,
               label="SCF 2025, income in 2024 (family)")
    ax.annotate(f"{v:.1f}", (2025, v), xytext=(7, 0), textcoords="offset points", fontsize=7.8, color=INK2,
                va="center")
    if grp == "top20":
        ce22 = ts("CE Table 1101 (quintiles)", "top20", 2022)
        ax.plot([2022, 2025], [ce22, z22.zandi_share_2025_nominal_pct], color=BLUE, lw=1.2, ls=(0, (4, 3)),
                zorder=3, label="CE if Zandi's split held from 2022")
        ax.annotate(f"{z22.zandi_share_2025_nominal_pct:.1f}", (2025, z22.zandi_share_2025_nominal_pct),
                    xytext=(6, 0), textcoords="offset points", fontsize=7.8, color=INK2, va="center")
        ax.set_ylim(31, 45)
    else:
        ax.set_ylim(17, 31)
    ax.set_xlim(1999.5, 2026.3)
    ax.set_title(ttl, loc="left", fontsize=9.5)
    ax.text(2022.6, ax.get_ylim()[1] - 0.25, "2023-25", fontsize=7.2, color=MUTED, va="top")
h, l = axes[1].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.005), fontsize=8)
fig.suptitle("Top spending shares in four official distributions: different levels, no rise after 2022",
             x=0.06, ha="left", fontsize=11, fontweight="bold", y=0.985)
fig.text(0.06, 0.905, "Levels differ because the sources rank by different things (income, spending, disposable "
         "income), equivalize or not, and cover different spending\n(CE out-of-pocket incl. pensions; PCE; SCF "
         "non-housing). Shaded: the years of Zandi's claim that official distributions reach. BEA-BLS joint shown "
         "from 2004, as BEA's page provides it.", fontsize=7.8, color=INK2, va="bottom")
fig.subplots_adjust(top=0.81, bottom=0.17, left=0.06, right=0.97)
fig.savefig(FIG / "fig_direct_top_shares.png", dpi=200)
plt.close(fig)

# --- figure 2: DFA equity holdings by income group, and the wealth-effect bound ------------------------------
eq = DFA[(DFA.category == "Corporate equities and mutual fund shares") & (DFA.measure == "level")].copy()
eq["value"] = eq.value.astype(float) / 1e6                         # $ trillion
eq = eq.pivot_table(index="date", columns="group", values="value")
eq = eq[eq.index >= "2015Q1"]
eq["bottom80"] = eq[DFA_GROUPS[:4]].sum(axis=1)
qx = np.array([int(d[:4]) + (int(d[-1]) - 0.5) / 4 for d in eq.index])
fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.4), gridspec_kw=dict(wspace=0.22, width_ratios=[1.05, 1]))
ax = axes[0]
style_axes(ax)
x0 = 2022 + 2.5 / 4
ax.axvspan(x0, qx.max() + 0.1, color=GRID, alpha=0.55, lw=0, zorder=0)
ax.text(x0 + 0.08, 0.5, "DFA model extrapolation\n(SCF 2025 not yet in)", fontsize=7.4, color=MUTED, va="bottom")
for g, col, lab in (("pct99to100", ORANGE, "Top 1% (99-100)"), ("pct80to99", BLUE, "80-99"),
                    ("bottom80", AQUA, "Bottom 80%")):
    ax.plot(qx, eq[g], color=col, lw=1.8, solid_capstyle="round", label=lab, zorder=3)
    ax.scatter(qx[-1], eq[g].iloc[-1], s=30, color=col, edgecolor=SURF, linewidth=1.4, zorder=4)
    ax.annotate(f"${eq[g].iloc[-1]:.1f}tn", (qx[-1], eq[g].iloc[-1]), xytext=(6, 0), textcoords="offset points",
                fontsize=7.8, color=INK2, va="center")
ax.set_xlim(2015, 2027.4)
ax.set_ylim(0, None)
ax.set_title("Corporate equities and mutual fund shares, by income group, $ trillion", loc="left", fontsize=9.5)
ax.legend(loc="upper left", fontsize=8)
ax = axes[1]
style_axes(ax)
pos = np.arange(len(DFA_GROUPS))
GCOL = {"pct00to20": AQUA, "pct20to40": AQUA, "pct40to60": AQUA, "pct60to80": AQUA, "pct80to99": BLUE,
        "pct99to100": ORANGE}                                   # same entities and colors as the left panel
for k, (w, alpha) in enumerate((("2022Q3->2025Q2", 0.45), ("2022Q3->2026Q2", 1.0))):
    x = WE[(WE.window == w) & (WE.base == "equities (revaluation share applied)") &
           WE.denominator.str.startswith("SCF")].pivot_table(index="group", columns="c_w",
                                                             values="pct_of_group_spending")
    x = x.loc[DFA_GROUPS]
    xp = pos + (k - 0.5) * 0.34
    ax.bar(xp, x[CW["central"]], width=0.3, color=[GCOL[g] for g in DFA_GROUPS], alpha=alpha, zorder=3)
    ax.vlines(xp, x[CW["low"]], x[CW["high"]], color=INK2, lw=1.0, zorder=4)
    for xi, v, hi in zip(xp, x[CW["central"]], x[CW["high"]]):
        ax.annotate(f"{v:.1f}", (xi, hi), xytext=(0, 3), textcoords="offset points", fontsize=7.2, color=INK2,
                    ha="center", va="bottom")
ax.set_xticks(pos, [DFA_LABEL[g] for g in DFA_GROUPS])
ax.set_xlabel("Income group (percentiles, SCF family income as in the DFA)", fontsize=8)
ax.set_title("Hypothetical wealth-effect spending, % of the group's spending", loc="left", fontsize=9.5)
gA, gB = weg("2022Q3->2025Q2", CW["central"], "SCF"), weg("2022Q3->2026Q2", CW["central"], "SCF")
bA, bB = weg("2022Q3->2025Q2", CW["central"], "BEA"), weg("2022Q3->2026Q2", CW["central"], "BEA")
ax.text(0.02, 0.97, f"Bars: 3.5 cents per dollar of equity revaluation gain per year; whiskers: 2-5 cents.\n"
        f"Implied top 20% minus bottom 80% gap: {gA:.1f} pts by 2025Q2, {gB:.1f} by 2026Q2\n"
        f"(BEA-BLS spending shares as denominators: {bA:.1f} and {bB:.1f}).\n"
        f"Observed (CE, real, 2022-25): {gap('quintile', '2022->2025'):+.1f} pts; Zandi: "
        f"{gap('quintile', '2022->2025', 'zandi_gap_pts'):+.1f} over three years.",
        transform=ax.transAxes, fontsize=7.6, color=INK2, va="top")
ax.legend([Patch(color=INK2, alpha=0.45), Patch(color=INK2)], ["light: gains 2022Q3 to 2025Q2 (lines up with CE "
           "2022-25)", "full: gains 2022Q3 to 2026Q2 (latest)"], loc="upper left", bbox_to_anchor=(0.0, 0.8),
          fontsize=7.8)
ax.set_ylim(0, 52)
fig.suptitle("Equity gains went to the top; what a 2-5 cent wealth effect would do with them (an assumption, "
             "not a measurement)", x=0.06, ha="left", fontsize=11, fontweight="bold", y=0.995)
fig.text(0.06, 0.006, "Sources: Fed Distributional Financial Accounts (2026:Q2, released 2026-09-18), equities exclude "
         "DC pensions; Z.1 S1M revaluation share of the change in household equity holdings; SCF 2025 non-housing "
         "spending shares by the same income groups, scaled to PCE. Uniform propensity across groups; no lags.",
         fontsize=7.2, color=MUTED, wrap=True)
fig.subplots_adjust(top=0.9, bottom=0.15, left=0.06, right=0.98)
fig.savefig(FIG / "fig_direct_dfa_equity.png", dpi=200)
plt.close(fig)

# --- figure 3: SCF 2025 windfall allocations by usual income, liquidity and hand-to-mouth status ---------------
def stacked(ax, df, labels, title):
    style_axes(ax)
    ax.grid(axis="y", visible=False)
    y = np.arange(len(df))[::-1]
    left = np.zeros(len(df))
    for c, col, nm in (("spend_pct", BLUE, "spend"), ("debt_pct", ORANGE, "pay down debt"),
                       ("save_pct", AQUA, "save")):
        v = df[c].values
        ax.barh(y, v - 0.6, left=left + 0.3, height=0.62, color=col, zorder=3, label=nm)   # 2px-like surface gaps
        if c == "spend_pct":
            for yi, vi, li in zip(y, v, left):
                ax.text(li + 1.2, yi, f"{vi:.0f}", color="#ffffff", fontsize=7.4, va="center", ha="left",
                        zorder=5)
        left = left + v
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 100)
    ax.set_title(title, loc="left", fontsize=9.2)
    return ax


WFI = WF[WF.grouping == "usual income, 12 groups"]
WFL = WF[WF.grouping == "liquidity, months of usual income"]
WFK = WF[WF.grouping == "hand-to-mouth (KVW-style, poor/wealthy)"]
fig = plt.figure(figsize=(12.4, 7.0))
gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1], height_ratios=[5, 3], wspace=0.42, hspace=0.42)
ax1 = fig.add_subplot(gs[:, 0])
stacked(ax1, WFI, [f"{g}" for g in WFI.group], "By usual income (percentile group), % of the windfall")
ax1.set_xlabel("% of a one-month windfall (family-weighted means)", fontsize=8)
gr = GRAD.set_index("grouping").loc["usual income, deciles"]
fig.text(0.08, 0.075, f"Spend share, top decile / bottom decile of usual income: {gr.ratio_spend:.2f} (95% family "
         f"bootstrap {gr.ratio_spend_lo95:.2f}-{gr.ratio_spend_hi95:.2f}). The post assumes an MPC of 1.0 at the "
         f"bottom falling to 0.40-0.65 at the top for a permanent flow\n(a ratio of 0.40-0.65). The SCF asks about a "
         f"one-off windfall, so it bears on the ordering of the post's gradient, not on its level or exact slope.",
         fontsize=7.6, color=INK2, va="bottom")
ax2 = fig.add_subplot(gs[0, 1])
stacked(ax2, WFL, ["<0.5 (hand-to-mouth)", "0.5-2", "2-6", "6-24", "24+"],
        "By liquid assets, months of usual income")
ax3 = fig.add_subplot(gs[1, 1])
stacked(ax3, WFK, list(WFK.group), "Hand-to-mouth status (KVW-style)")
h, l = ax1.get_legend_handles_labels()
fig.legend(h, l, loc="upper right", ncol=3, bbox_to_anchor=(0.98, 0.955), fontsize=8)
fig.suptitle("SCF 2025: what families say they would do with a windfall of one month's income",
             x=0.06, ha="left", fontsize=11, fontweight="bold", y=0.995)
fig.text(0.08, 0.012, "Source: SCF 2025 summary extract (Federal Reserve Board), MPSPEND/MPSAVE/MPDEBT, WGT over all "
         "implicates; reproduces the FEDS Note of 2026-10-09 (overall 22.35/47.31/30.30).\nLiquid assets as in the "
         "note (transaction accounts, CDs, directly held funds, stocks, bonds). KVW-style: net liquid wealth <= half "
         "a month of 2024 income; wealthy if illiquid wealth > 0.", fontsize=7.2, color=MUTED, va="bottom")
fig.subplots_adjust(top=0.88, bottom=0.2, left=0.08, right=0.98)
fig.savefig(FIG / "fig_direct_windfall.png", dpi=200)
plt.close(fig)
print("Charts done")

# %% 10. Generated tables for NOTES_direct.md (pasted there verbatim; check_direct.py verifies they match)
def md(df, floatfmt=None):
    cols = list(df.columns)
    out = ["| " + " | ".join(str(c) for c in cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        cells = []
        for c in cols:
            v = r[c]
            if isinstance(v, (float, np.floating)):
                f = (floatfmt or {}).get(c, "{:.1f}")
                cells.append("" if pd.isna(v) else f.format(v))
            else:
                cells.append(str(v))
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


TABLES = {}

# T1: top shares on one footing, 2019-2025
rows = []
for lab, src, grp in (("CE, income before taxes: top 10%", CED, "top10"),
                      ("CE, income before taxes: top 20%", CEQ, "top20"),
                      ("CE, excl. pensions, Social Security, contributions: top 20%", CEQ, "top20c"),
                      ("CE, SCF-like scope: top 10%", "CE Table 1110 (deciles), SCF-like scope", "top10"),
                      ("CE, SCF-like scope: top 20%", "CE Table 1101 (quintiles), SCF-like scope", "top20"),
                      ("BLS dPCE, equivalized spending: top 10%", DP1, "top10"),
                      ("BLS dPCE, equivalized spending: top 20%", DP2, "top20"),
                      ("BLS dPCE, equivalized spending: top 1%", "BLS distributional PCE (T2)", "top1"),
                      ("BEA-BLS joint, equivalized DPI: top 10%", JNT, "top10"),
                      ("BEA-BLS joint, equivalized DPI: top 20%", JNT, "top20"),
                      ("BEA-BLS joint, equivalized DPI: top 1%", JNT, "top1"),
                      ("SCF 2025 non-housing, income 2024: top 10%", SCF_MAIN, "top10"),
                      ("SCF 2025 non-housing, income 2024: top 20%", SCF_MAIN, "top20"),
                      ("SCF 2025 non-housing, income 2024: top 1%", SCF_MAIN, "top1"),
                      ("SCF 2025 non-housing, usual income: top 10% (Bulletin 28.5)",
                       "SCF 2025, total non-housing spending (TOTSPENDNH), ranked by usual income (NORMINC)", "top10")):
    g = "top20" if grp == "top20c" else grp
    x = TS[(TS.source == src) & (TS.group == g)].set_index("year")
    col = "share_consumption_pct" if grp == "top20c" else "share_pct"
    r = {"Source and group": lab}
    for y in range(2019, 2026):
        r[str(y)] = x[col].get(y, np.nan)
    last = max(y for y in range(2019, 2026) if not pd.isna(r[str(y)]))
    r["Change 2022 to last, pts"] = r[str(last)] - r["2022"] if not pd.isna(r["2022"]) else np.nan
    se = (np.hypot(x.se_pct.get(2022, np.nan), x.se_pct.get(last, np.nan))
          if src in (CED, CEQ) and grp != "top20c" else np.nan)
    r["Approx. SE of the change, pts"] = se
    rows.append(r)
TABLES["T1_top_shares"] = md(pd.DataFrame(rows), {"Change 2022 to last, pts": "{:+.1f}",
                                                  "Approx. SE of the change, pts": "{:.2f}"})

foot = pd.DataFrame([dict(Source=k, Ranking=v["ranking"], Equivalized=v["equivalized"], Unit=v["unit"],
                          Scope=v["scope"], **{"Top tail": v["top_tail"]})
                     for k, v in (("CE (BLS)", FOOTING["CE"]), ("BLS dPCE", FOOTING["dPCE"]),
                                  ("BEA-BLS joint", FOOTING["joint"]), ("SCF 2025 (Fed)", FOOTING["SCF"]))])
TABLES["T1b_footing"] = md(foot)

# T2: CE quintiles, nominal and real means, growth
lq = LEV_Q.set_index(["group", "year"])
rows = []
for g, lab in (("q1", "Q1"), ("q2", "Q2"), ("q3", "Q3"), ("q4", "Q4"), ("q5", "Q5 (top 20%)"),
               ("bottom80", "Bottom 80%"), ("all", "All CUs")):
    r = {"Group": lab}
    for y in (2019, 2022, 2023, 2024, 2025):
        r[f"{y} nominal $"] = lq.loc[(g, y), "mean_total"]
    r["2025 real (2024 $)"] = lq.loc[(g, 2025), "mean_total_real2024"]
    for w in ("2022->2025", "2023->2025"):
        x = GR[(GR.grouping == "quintile") & (GR.group == g) & (GR.window == w)].iloc[0]
        r[f"Real mean {w.replace('->', '-')}, %"] = x.g_mean_total_real2024
        r[f"Real aggregate {w.replace('->', '-')}, %"] = x.g_agg_bn_total_real2024
    r["Real agg. 2022-2025 excl. pensions/contrib., %"] = GR[(GR.grouping == "quintile") & (GR.group == g) &
                                                            (GR.window == "2022->2025")].g_agg_bn_consumption_real2024.iloc[0]
    rows.append(r)
TABLES["T2_ce_quintiles"] = md(pd.DataFrame(rows), {**{f"{y} nominal $": "{:,.0f}" for y in (2019, 2022, 2023, 2024, 2025)},
                                                    "2025 real (2024 $)": "{:,.0f}"})

rows = []
for g in DS + ["top10", "bottom90"]:
    r = {"Decile": g.upper() if g.startswith("d") else {"top10": "Top 10%", "bottom90": "Bottom 90%"}[g]}
    ld = LEV_D.set_index(["group", "year"])
    r["2022 nominal $"] = ld.loc[(g, 2022), "mean_total"]
    r["2025 nominal $"] = ld.loc[(g, 2025), "mean_total"]
    for w in ("2022->2025", "2023->2025"):
        x = GR[(GR.grouping == "decile") & (GR.group == g) & (GR.window == w)].iloc[0]
        r[f"Real mean {w.replace('->', '-')}, %"] = x.g_mean_total_real2024
        r[f"Real aggregate {w.replace('->', '-')}, %"] = x.g_agg_bn_total_real2024
        r[f"approx. SE {w.replace('->', '-')}"] = x.se_g_agg_bn_total_real2024
    rows.append(r)
TABLES["T2b_ce_deciles"] = md(pd.DataFrame(rows), {"2022 nominal $": "{:,.0f}", "2025 nominal $": "{:,.0f}"})

rows = []
for r_ in GAPS.itertuples():
    rows.append({"Groups": f"{r_.top} vs {r_.bottom}", "Window": r_.window.replace("->", "-"),
                 "Top real %": r_.top_real_total, "Rest real %": r_.bottom_real_total,
                 "Gap, pts": r_.gap_real_total_pts, "Approx. SE, pts": r_.se_gap_pts,
                 "Gap excl. pensions/contrib., pts": r_.gap_real_consumption_pts,
                 "Zandi's gap, pts": r_.zandi_gap_pts})
TABLES["T3_ce_gaps"] = md(pd.DataFrame(rows), {"Gap, pts": "{:+.1f}", "Gap excl. pensions/contrib., pts": "{:+.1f}"})

TABLES["T3b_zandi_arithmetic"] = md(ZARITH.rename(columns={"item": "Item", "share_top20_pct": "Top-20 share, %",
                                                           "pct_a_year": "% a year"}))

rows = []
for r_ in ZSH.itertuples():
    rows.append({"Base year": int(r_.base_year), "Top-20% share in base year, %": r_.share_base_pct,
                 "Zandi's split, 2025 (real), %": r_.zandi_share_2025_real_pct,
                 "Zandi's split, 2025 (nominal), %": r_.zandi_share_2025_nominal_pct,
                 "Observed 2025, %": r_.observed_share_2025_pct,
                 "Zandi minus observed, pts": r_.zandi_minus_observed_pts,
                 "Approx. SE of the change, pts": r_.se_change_pts,
                 "Zandi minus observed, SEs": r_.zandi_minus_observed_in_ses,
                 "Same, excl. pensions/contrib.: Zandi / observed, %":
                     f"{r_.zandi_consumption_share_2025_nominal_pct:.1f} / {r_.observed_consumption_share_2025_pct:.1f}"})
TABLES["T4_zandi_share"] = md(pd.DataFrame(rows), {"Base year": "{:.0f}", "Approx. SE of the change, pts": "{:.2f}"})

c = COMP[COMP.window == "2022->2025"].pivot_table(index="item", columns="group",
                                                   values=["share_start_pct", "share_end_pct", "change_share_pts",
                                                           "growth_nominal_pct"], sort=False)
rows = []
for it in [i for i, _ in COMP_ITEMS] + ["Total (sum of items)"]:
    rows.append({"Item": it,
                 "Q1 share 2022, %": c.loc[it, ("share_start_pct", "q1")], "Q1 2025, %": c.loc[it, ("share_end_pct", "q1")],
                 "Q1 change, pts": c.loc[it, ("change_share_pts", "q1")],
                 "Q1 growth, %": c.loc[it, ("growth_nominal_pct", "q1")],
                 "Q5 share 2022, %": c.loc[it, ("share_start_pct", "q5")], "Q5 2025, %": c.loc[it, ("share_end_pct", "q5")],
                 "Q5 change, pts": c.loc[it, ("change_share_pts", "q5")],
                 "Q5 growth, %": c.loc[it, ("growth_nominal_pct", "q5")]})
TABLES["T5_composition"] = md(pd.DataFrame(rows), {"Q1 change, pts": "{:+.2f}", "Q5 change, pts": "{:+.2f}",
                                                   "Q1 growth, %": "{:+.0f}", "Q5 growth, %": "{:+.0f}"})

# T6: income side
pq = PIQ.set_index(["group", "year"])
rows = []
for g, lab in (("q1", "Q1"), ("q2", "Q2"), ("q3", "Q3"), ("q4", "Q4"), ("q5", "Q5 (top 20%)"),
               ("bottom80", "Bottom 80%"), ("all", "All")):
    r = {"Group": lab}
    for y in range(2019, 2026):
        r[{2024: "2024 (prov.)", 2025: "2025 (nowcast)"}.get(y, str(y))] = pq.loc[(g, y), "share"]
    for w in ("2019->2024", "2022->2025", "2023->2025", "2024->2025"):
        r[f"Real {w.replace('->', '-')}, %"] = incg("Personal income", g, w)
    r["Nominal 2024-2025, %"] = incg("Personal income", g, "2024->2025", "g_nominal_pct")
    rows.append(r)
TABLES["T6_personal_income"] = md(pd.DataFrame(rows), {c: "{:.3f}" for c in ("2019", "2020", "2021", "2022",
                                                                              "2023", "2024 (prov.)",
                                                                              "2025 (nowcast)")})

# T6b: disposable income by quintile of equivalized DPI (what spending is paid from; ends in 2024), with taxes
dq = DPIQ.set_index(["group", "year"])
rows = []
for g, lab in (("q1", "Q1"), ("q2", "Q2"), ("q3", "Q3"), ("q4", "Q4"), ("q5", "Q5 (top 20%)"),
               ("bottom80", "Bottom 80%"), ("all", "All")):
    r = {"Group": lab}
    for y in (2019, 2022, 2023, 2024):
        r[f"DPI share {y}" + (" (prov.)" if y == 2024 else "")] = dq.loc[(g, y), "share"]
    for w in ("2019->2024", "2022->2023", "2023->2024", "2022->2024"):
        r[f"Real DPI {w.replace('->', '-')}, %"] = incg("Disposable personal income", g, w)
    gt = "top20" if g == "q5" else g
    r["Taxes 2022, $bn"] = taxes(gt, 2022, "taxes_bn")
    r["Taxes 2024, $bn"] = taxes(gt, 2024, "taxes_bn")
    for y in (2022, 2023, 2024):
        r[f"Taxes, % of PI {y}"] = taxes(gt, y)
    rows.append(r)
TABLES["T6b_disposable_income"] = md(pd.DataFrame(rows), {**{c: "{:.3f}" for c in ("DPI share 2019", "DPI share 2022",
                                                                                    "DPI share 2023",
                                                                                    "DPI share 2024 (prov.)")},
                                                          "Taxes 2022, $bn": "{:,.0f}", "Taxes 2024, $bn": "{:,.0f}"})

# T6c: income concept against ranking, top 20% vs bottom 80% (real)
rows = []
for concept, rk, lab in (("Personal income", "equivalized_pi", "Personal income, ranked by equivalized PI (main)"),
                         ("Personal income", "equivalized_dpi", "Personal income, ranked by equivalized DPI"),
                         ("Disposable personal income", "equivalized_pi", "Disposable income, ranked by equivalized PI"),
                         ("Disposable personal income", "equivalized_dpi",
                          "Disposable income, ranked by equivalized DPI (main)")):
    r = {"Concept and ranking": lab}
    for w in ("2022->2024", "2022->2023", "2023->2024"):
        t_, b_ = incg(concept, "top20", w, ranking=rk), incg(concept, "bottom80", w, ranking=rk)
        r[f"{w.replace('->', '-')}: top 20%, %"] = t_
        r[f"{w.replace('->', '-')}: bottom 80%, %"] = b_
        r[f"{w.replace('->', '-')}: gap, pts"] = t_ - b_
    rows.append(r)
TABLES["T6c_concept_vs_ranking"] = md(pd.DataFrame(rows), {c: "{:+.1f}" for c in (
    "2022-2024: gap, pts", "2022-2023: gap, pts", "2023-2024: gap, pts")})

jr = JOINT_ROWS.set_index(["group", "year"])
rows = []
for g, lab in [(f"D{k:02d}", f"D{k}") for k in range(1, 11)] + [("B80", "Bottom 80%"), ("Q5", "Top 20%"),
                                                                  ("T05", "Top 5%"), ("T01", "Top 1%"), ("ALL", "All")]:
    r = {"DPI group": lab + ("" if not pd.isna(jr.loc[(g, 2019), "saving_rate_published"]) else " (from shares)")}
    for y in range(2019, 2024):
        pub = jr.loc[(g, y), "saving_rate_published"]          # BEA's published rate where it exists
        r[f"Saving rate {y}, %"] = 100 * (pub if not pd.isna(pub) else jr.loc[(g, y), "saving_rate_from_shares"])
    r["Change 2019-2023, pts"] = r["Saving rate 2023, %"] - r["Saving rate 2019, %"]
    r["PCE/DPI 2019"] = jr.loc[(g, 2019), "pce_to_dpi"]
    r["PCE/DPI 2023"] = jr.loc[(g, 2023), "pce_to_dpi"]
    rows.append(r)
TABLES["T7_joint_saving"] = md(pd.DataFrame(rows), {"Change 2019-2023, pts": "{:+.1f}", "PCE/DPI 2019": "{:.2f}",
                                                    "PCE/DPI 2023": "{:.2f}"})

srows = [{"Period": str(y), "Saving rate, % of DPI": SR_A[y]} for y in range(2019, 2026)]
srows += [{"Period": d, "Saving rate, % of DPI": SR_M[d]} for d in [f"2026-{m:02d}" for m in range(1, 10)]]
TABLES["T8_saving_rate"] = md(pd.DataFrame(srows))

# T9: DFA levels and gains
rows = []
for cat in ("Net worth", "Corporate equities and mutual fund shares", "Real estate", "Consumer credit"):
    for g in DFA_GROUPS + ["top20", "bottom80", "all"]:
        x = DFA_ROWS[(DFA_ROWS.category == cat) & (DFA_ROWS.group == g)].set_index("date")
        rows.append({"Item": cat, "Income group": DFA_LABEL.get(g, {"top20": "Top 20%", "bottom80": "Bottom 80%",
                                                                       "all": "All"}.get(g)),
                     "2019Q4, $bn": x.loc["2019Q4", "level_bn"], "2022Q3, $bn": x.loc["2022Q3", "level_bn"],
                     "2026Q2, $bn": x.loc["2026Q2", "level_bn"],
                     "Change 2022Q3-2026Q2, $bn": x.loc["2026Q2", "level_bn"] - x.loc["2022Q3", "level_bn"],
                     "Change, %": 100 * (x.loc["2026Q2", "level_bn"] / x.loc["2022Q3", "level_bn"] - 1),
                     "Share 2026Q2, %": x.loc["2026Q2", "share_pct"],
                     "Per household 2026Q2, $k": x.loc["2026Q2", "per_household_k"]})
TABLES["T9_dfa"] = md(pd.DataFrame(rows), {"2019Q4, $bn": "{:,.0f}", "2022Q3, $bn": "{:,.0f}", "2026Q2, $bn": "{:,.0f}",
                                           "Change 2022Q3-2026Q2, $bn": "{:+,.0f}", "Change, %": "{:+.0f}",
                                           "Per household 2026Q2, $k": "{:,.0f}"})

# T10: wealth-effect bound
rows = []
for w in ("2022Q3->2025Q2", "2022Q3->2026Q2"):
    for den in SPEND_SHARE:
        x = WE[(WE.window == w) & (WE.base == "equities (revaluation share applied)") & (WE.denominator == den)]
        for g in DFA_GROUPS + ["top20", "bottom80", "all"]:
            y = x[x.group == g].set_index("c_w")
            rows.append({"Window": w.replace("->", "-"), "Denominator": "SCF 2025 shares" if den.startswith("SCF")
                         else "BEA-BLS 2023 shares",
                         "Group": DFA_LABEL.get(g, {"top20": "Top 20%", "bottom80": "Bottom 80%", "all": "All"}.get(g)),
                         "Revaluation gain, $bn": GAINS[(GAINS.window == w) & (GAINS.base ==
                                                        "equities (revaluation share applied)") &
                                                       (GAINS.group == g)].gain_bn.iloc[0],
                         "Group spending, $bn": y.group_spending_bn.iloc[0],
                         "2 cents: % of group spending": y.loc[0.02, "pct_of_group_spending"],
                         "3.5 cents": y.loc[0.035, "pct_of_group_spending"],
                         "5 cents": y.loc[0.05, "pct_of_group_spending"],
                         "% of PCE at 2 / 3.5 / 5 cents": f"{y.loc[0.02, 'pct_of_pce']:.2f} / "
                                                          f"{y.loc[0.035, 'pct_of_pce']:.2f} / "
                                                          f"{y.loc[0.05, 'pct_of_pce']:.2f}"})
TABLES["T10_wealth_effect"] = md(pd.DataFrame(rows), {"Revaluation gain, $bn": "{:,.0f}",
                                                      "Group spending, $bn": "{:,.0f}"})
rows = []
for w in ("2022Q3->2025Q2", "2022Q3->2026Q2"):
    for base in ("equities (revaluation share applied)", "equities (level change)", "net worth (level change)"):
        r = {"Window": w.replace("->", "-"), "Gain counted": base}
        for den, dl_ in (("SCF", "SCF shares"), ("BEA", "BEA-BLS shares")):
            for cw in (0.02, 0.035, 0.05):
                r[f"{dl_}, {100 * cw:g} cents"] = weg(w, cw, den, base)
        rows.append(r)
TABLES["T10b_implied_gap"] = md(pd.DataFrame(rows))
REV = pd.DataFrame(REVAL.values())
TABLES["T10c_revaluation"] = md(REV.rename(columns={"window": "Window", "z1_level_start_bn": "Z.1 level start, $bn",
                                                    "z1_level_end_bn": "Z.1 level end, $bn",
                                                    "z1_change_bn": "Change, $bn",
                                                    "z1_revaluation_bn": "Revaluations, $bn",
                                                    "reval_share": "Revaluation share"}),
                                {"Z.1 level start, $bn": "{:,.0f}", "Z.1 level end, $bn": "{:,.0f}",
                                 "Change, $bn": "{:,.0f}", "Revaluations, $bn": "{:,.0f}", "Revaluation share": "{:.3f}"})
TABLES["T10d_runup_timing"] = md(RUNUP.rename(columns={
    "window": "Window", "quarters": "Quarters", "dfa_change_bn": "DFA equity holdings, change, $bn",
    "dfa_change_pct": "Change, %", "z1_revaluation_bn": "Z.1 revaluations, $bn",
    "dfa_change_bn_per_quarter": "DFA change per quarter, $bn",
    "z1_revaluation_bn_per_quarter": "Z.1 revaluations per quarter, $bn"}),
    {"Quarters": "{:.0f}", "DFA equity holdings, change, $bn": "{:+,.0f}", "Z.1 revaluations, $bn": "{:+,.0f}",
     "DFA change per quarter, $bn": "{:+,.0f}", "Z.1 revaluations per quarter, $bn": "{:+,.0f}"})

# T11: concentration, SCF survey against the DFA model
rows = []
x = CONC[CONC.dfa_quarter.notna() & CONC.group.isin(DFA_GROUPS)]
for (yr, con), y in x.groupby(["scf_year", "concept"], sort=False):
    y = y.set_index("group")
    r = {"SCF year (DFA quarter)": f"{int(yr)} ({y.dfa_quarter.iloc[0]})", "SCF concept": con}
    for g in DFA_GROUPS:
        r[DFA_LABEL[g]] = f"{y.loc[g, 'scf_share_pct']:.1f} / {y.loc[g, 'dfa_equities_share_pct']:.1f}"
    rows.append(r)
TABLES["T11_concentration"] = md(pd.DataFrame(rows))
rows = []
for r_ in CONC[CONC.concept.str.contains("share held")].itertuples():
    v = r_.scf_share_pct if not pd.isna(r_.scf_share_pct) else r_.dfa_equities_share_pct
    rows.append({"Measure": r_.concept, "Year": int(r_.scf_year) if not pd.isna(r_.scf_year) else r_.dfa_quarter,
                 "Share, %": v})
TABLES["T11b_equity_top"] = md(pd.DataFrame(rows))

# T12: windfall
x = WF[WF.grouping == "usual income, 12 groups"]
def wrow(lab, r_):
    return {"Usual income": lab, "Spend %": r_.spend_pct, "Spend % (publisher)": r_.publisher_spend_pct,
            "Save %": r_.save_pct, "Save % (publisher)": r_.publisher_save_pct, "Pay debt %": r_.debt_pct,
            "Pay debt % (publisher)": r_.publisher_debt_pct, "SE spend (bootstrap)": r_.se_spend_boot,
            "Spend nothing, % of families": r_.share_spend_none_pct, "Mean windfall, $": r_.mean_windfall_usd}


rows = [wrow(r_.group, r_) for r_ in x.itertuples()] + [wrow("All families", WF[WF.grouping == "all"].iloc[0])]
TABLES["T12_windfall_income"] = md(pd.DataFrame(rows), {c: "{:.2f}" for c in (
    "Spend %", "Spend % (publisher)", "Save %", "Save % (publisher)", "Pay debt %", "Pay debt % (publisher)",
    "SE spend (bootstrap)")} | {"Mean windfall, $": "{:,.0f}"})
rows = []
for gname in ("income 2024, deciles", "usual income, deciles", "net worth, deciles"):
    for r_ in WF[WF.grouping == gname].itertuples():
        rows.append({"Ranking": gname.split(",")[0], "Decile": r_.group, "Spend %": r_.spend_pct,
                     "Save %": r_.save_pct, "Pay debt %": r_.debt_pct, "Spend + debt %": r_.spend_plus_debt_pct,
                     "Spend, income-weighted %": r_.spend_income_weighted_pct, "SE spend": r_.se_spend_boot})
TABLES["T12b_windfall_deciles"] = md(pd.DataFrame(rows), {"SE spend": "{:.2f}"})
rows = []
for gname in ("hand-to-mouth (FEDS Note definition)", "hand-to-mouth (KVW-style, poor/wealthy)",
              "liquidity, months of usual income", "hand-to-mouth x usual-income quintile",
              "spending vs income last year (WSAVED)", "hand-to-mouth, regression-adjusted (FEDS Note Fig. 4 recipe)"):
    for r_ in WF[WF.grouping == gname].itertuples():
        rows.append({"Grouping": gname, "Group": r_.group, "Families, m": r_.families_m, "Spend %": r_.spend_pct,
                     "Save %": r_.save_pct, "Pay debt %": r_.debt_pct, "SE spend": r_.se_spend_boot,
                     "Publisher spend %": r_.publisher_spend_pct})
TABLES["T12c_windfall_liquidity"] = md(pd.DataFrame(rows), {"SE spend": "{:.2f}"})
rows = [{"Ranking": r_.grouping, "Top": r_.top, "Bottom": r_.bottom, "Spend top %": r_.spend_top,
         "Spend bottom %": r_.spend_bottom, "Ratio": r_.ratio_spend,
         "95% (family bootstrap)": f"{r_.ratio_spend_lo95:.2f}-{r_.ratio_spend_hi95:.2f}",
         "Ratio, spend + debt": r_.ratio_spend_plus_debt, "Ratio, income-weighted": r_.ratio_income_weighted,
         "Post's ratio": f"{r_.post_ratio_lo:.2f}-{r_.post_ratio_hi:.2f}"} for r_ in GRAD.itertuples()]
TABLES["T12d_gradient"] = md(pd.DataFrame(rows), {"Ratio": "{:.2f}", "Ratio, spend + debt": "{:.2f}",
                                                  "Ratio, income-weighted": "{:.2f}"})

# T13: SCF spending against the Bulletin; the CE-SCF scope bridge
rows = []
for r_ in SP[SP.bulletin_mean.notna() | SP.bulletin_share_pct.notna()].itertuples():
    rows.append({"Grouping": r_.grouping, "Group": r_.group, "Mean, $": r_.mean_totspendnh,
                 "Bulletin mean, $": r_.bulletin_mean, "Share of aggregate, %": r_.share_of_aggregate_pct,
                 "Bulletin share, %": r_.bulletin_share_pct})
TABLES["T13_scf_bulletin"] = md(pd.DataFrame(rows), {"Mean, $": "{:,.0f}", "Bulletin mean, $": "{:,.0f}"})
n25 = ce_counts(CE_D, 2025)["all"]
ce_tot = n25 * ce_cell(CE_D, 2025, "all", TOT) / 1e6
ce_scope = n25 * (ce_cell(CE_D, 2025, "all", TOT) - ce_cell(CE_D, 2025, "all", OWN) - ce_cell(CE_D, 2025, "all", RNT) -
                  ce_cell(CE_D, 2025, "all", PIP) - ce_cell(CE_D, 2025, "all", CASH)) / 1e6
BRIDGE = pd.DataFrame([
    {"Measure (2025)": "CE average annual expenditures (all CUs)", "Aggregate, $tn": ce_tot / 1e3,
     "Top 10%, %": ts(CED, "top10", 2025), "Top 20%, %": ts(CEQ, "top20", 2025)},
    {"Measure (2025)": "CE, SCF-like scope (minus owned and rented dwellings, pensions and insurance, cash "
                       "contributions)", "Aggregate, $tn": ce_scope / 1e3,
     "Top 10%, %": ts("CE Table 1110 (deciles), SCF-like scope", "top10", 2025),
     "Top 20%, %": ts("CE Table 1101 (quintiles), SCF-like scope", "top20", 2025)},
    {"Measure (2025)": "SCF 2025 total non-housing spending (income 2024 ranking)",
     "Aggregate, $tn": (S.TOTSPENDNH * S.WGT).sum() / 1e12, "Top 10%, %": ts(SCF_MAIN, "top10", 2025),
     "Top 20%, %": ts(SCF_MAIN, "top20", 2025)},
    {"Measure (2025)": "PCE (NIPA Table 2.1, calendar 2025)", "Aggregate, $tn": PCE_2025_TN, "Top 10%, %": np.nan,
     "Top 20%, %": np.nan},
])
TABLES["T13b_scope_bridge"] = md(BRIDGE, {"Aggregate, $tn": "{:.2f}"})

ev = EVID.rename(columns={"source": "Source", "ranking": "Ranking", "years": "Years",
                          "what_it_shows_top_vs_rest": "What it shows for the top vs the rest",
                          "consistent_with_zandi_split": "Consistent with Zandi's split?", "caveat": "Caveat"})
TABLES["T14_evidence"] = md(ev)

# T15: how fast would a top group the CE misses have to grow for Zandi's top-20% gap to hold? (arithmetic, not data)
# Top 20% gap = [S_h (g_h - g_b80) + (S20 - S_h) gap_seen] / S20, with S from SCF 2025 (income 2024 ranking) and
# gap_seen = what CE shows for its top quintile against its bottom 80% (2022-2025, real).
S20 = ts(SCF_MAIN, "top20", 2025)
HID = []
for hid, sh_h in (("top 1%", ts(SCF_MAIN, "top1", 2025)), ("top 5%", ts(SCF_MAIN, "top5", 2025)),
                  ("top 10%", ts(SCF_MAIN, "top10", 2025))):
    for lab, seen in (("total expenditures", gap("quintile", "2022->2025")),
                      ("excl. pensions and contributions", gap("quintile", "2022->2025", "gap_real_consumption_pts"))):
        zg = float(GAPS[(GAPS.grouping == "quintile") & (GAPS.window == "2022->2025")].zandi_gap_pts.iloc[0])
        need = (S20 * zg - (S20 - sh_h) * seen) / sh_h
        HID.append({"Group the CE misses": hid, "Its share of spending (SCF 2025), %": sh_h,
                    "CE gap for the rest of the top 20%, pts": seen, "CE concept": lab,
                    "Gap that group needs over 2022-2025, pts": need,
                    # annualizes 1 + gap: the group's own growth a year only if the bottom 80% were flat
                    "Per year if the bottom 80% were flat, %": 100 * ((1 + need / 100) ** (1 / 3) - 1)})
HID = pd.DataFrame(HID)
TABLES["T15_hidden_top"] = md(HID, {"CE gap for the rest of the top 20%, pts": "{:+.1f}"})

# T15b: like with like. The top 1%'s need and the wealth-effect bound on the top 1% depend on the spending shares
# used (SCF 2025 puts 6.3% of spending with the top 1% by income, the BEA-BLS joint distribution 2.1% by DPI); the
# comparison holds when both use the same shares, and mixing them would reverse it.
we1 = WE[(WE.window == "2022Q3->2025Q2") & (WE.base == "equities (revaluation share applied)") &
         (WE.group == "pct99to100")]
zg3, seen3 = gap("quintile", "2022->2025", "zandi_gap_pts"), gap("quintile", "2022->2025")
HW = {"SCF": (ts(SCF_MAIN, "top20", 2025), ts(SCF_MAIN, "top1", 2025)),
      "BEA": (ts(JNT, "top20", 2023), ts(JNT, "top1", 2023))}
HIDB = []
for lab, wk, bk in (("SCF 2025 shares for both", "SCF", "SCF"),
                    ("BEA-BLS 2023 shares for both", "BEA", "BEA"),
                    ("Mixed: SCF-weighted need, BEA-BLS bound", "SCF", "BEA")):
    s20, s1 = HW[wk]
    nd = (s20 * zg3 - (s20 - s1) * seen3) / s1
    bd = we1[we1.denominator.str.startswith(bk)].set_index("c_w").pct_of_group_spending
    HIDB.append({"Weights": lab, "Top 20% share, %": s20, "Top 1% share, %": s1,
                 "Gap the top 1% needs, 2022-2025, pts": nd,
                 "Bound on the top 1% by 2025Q2 at 2 / 3.5 / 5 cents, % of its spending":
                     f"{bd[0.02]:.1f} / {bd[0.035]:.1f} / {bd[0.05]:.1f}",
                 "Need above the 5-cent bound?": "yes" if nd > bd[0.05] else "no"})
HIDB = pd.DataFrame(HIDB)
TABLES["T15b_hidden_top_like_with_like"] = md(HIDB, {"Gap the top 1% needs, 2022-2025, pts": "{:.0f}"})

# T16: the aggregate saving rate against the wealth-effect bound, in points of DPI
DPI_M = pi_series(27)
dpi26q2 = DPI_M.loc[["2026-04", "2026-05", "2026-06"]].mean() / 1e3
sr_2324 = (SR_A[2023] + SR_A[2024]) / 2
sr_26q3 = SR_M.loc[["2026-07", "2026-08", "2026-09"]].mean()
SRX = [{"Item": "Saving rate, 2023-2024 average of annual rates, % of DPI", "Value": sr_2324},
       {"Item": "Saving rate, 2026Q3 (Jul-Sep monthly average), % of DPI", "Value": sr_26q3},
       {"Item": "Change, pts of DPI", "Value": sr_26q3 - sr_2324}]
# like with like: the 2023-24 saving rate already contains the wealth effect of gains up to then, so the change in
# saving since then is set against the gains accrued since the 2023-2024 average level of equity holdings
eq_all = DFA_LEV.xs("Corporate equities and mutual fund shares", level="category")["all"] / 1e3
eq_base = eq_all.loc[[f"{y}Q{k}" for y in (2023, 2024) for k in (1, 2, 3, 4)]].mean()
gain_inc = (eq_all.loc["2026Q2"] - eq_base) * REVAL["2022Q3->2026Q2"]["reval_share"]
SRX.append({"Item": "Household equity holdings (DFA), 2023-2024 average, $bn", "Value": eq_base})
SRX.append({"Item": "Revaluation gain from that average to 2026Q2 (Z.1 2022Q3-2026Q2 revaluation share applied), $bn",
            "Value": gain_inc})
for cwk, cw in CW.items():
    SRX.append({"Item": f"Wealth effect of that gain at {100 * cw:g} cents, % of DPI (2026Q2)",
                "Value": 100 * cw * gain_inc / dpi26q2})
SRX = pd.DataFrame(SRX)
SRX = SRX.assign(Value=[f"{v:,.0f}" if abs(v) > 100 else f"{v:.2f}" for v in SRX.Value])
# sensitivity: the revaluation share of the window that starts nearer the 2023-24 base
gain_alt = (eq_all.loc["2026Q2"] - eq_base) * REVAL["2024Q2->2026Q2"]["reval_share"]
SRX.loc[len(SRX)] = {"Item": "Same at 2 / 3.5 / 5 cents with the 2024Q2-2026Q2 revaluation share "
                             f"({REVAL['2024Q2->2026Q2']['reval_share']:.3f}), % of DPI",
                     "Value": " / ".join(f"{100 * cw * gain_alt / dpi26q2:.2f}" for cw in CW.values())}
TABLES["T16_saving_vs_bound"] = md(SRX)

with open(OUT / "direct_notes_tables.md", "w", encoding="utf-8") as fh:
    for k, v in TABLES.items():
        fh.write(f"<!-- {k} -->\n{v}\n\n")
print("Notes tables written:", len(TABLES))
print(f"PCE price index 2024->2025 used for 2025: {100 * (PCE_INFL_2025 - 1):.2f}%; saving-financed share of the "
      f"PCE rise Mar-Sep 2026: {SAV_FIN_SHARE:.1f}%")
