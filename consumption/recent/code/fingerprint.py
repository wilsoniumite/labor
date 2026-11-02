# fingerprint.py - Q2, by income group: is US spending being held up by higher incomes, and can the
# national accounts see it? (consumption/recent; Stella's question 2, second angle)
#
# Idea (Stella's). If spending is held up by the top, the categories the top buys should outgrow the
# categories the bottom buys in the national accounts (comprehensive; no survey top-coding).
#
# Model. theta_qg = group q's market share of category g (its share of all spending on g), x_q = growth of
# group q's total spending, eta_gq = Engel elasticity. If each group's spending on g grows by eta_gq * x_q,
#     g_g = sum_q theta_qg * eta_gq * x_q + e_g,
# with e_g collecting relative-price / substitution, supply shocks and taste shifts common to all groups.
# The x_q are identified from the cross-section of categories because categories differ in who buys them.
# Main specification: two groups (top 20% vs bottom 80%, Zandi's split), eta = 1:
#     g_g = x_b80 + theta_top20,g * (x_top20 - x_b80) + e_g        (WLS, base-period spending weights)
# so the slope on theta_top20 is the top20-bottom80 gap. Then 4 and 5 groups (ridge toward equal growth,
# lambda by leave-one-out CV; unconstrained OLS shown for reference), robustness drops and a placebo.
#
# Why the inverse model and not a fixed-share "basket" index: a K can work within categories (the top buying
# more of everything). A fixed-market-share basket attributes each category's growth to whoever already buys
# it, so it reads a K as a tiny tilt. With the same weights the basket gap is exactly
#     basket_gap = kappa * slope,   kappa = Var_w(theta) / (theta_bar * (1 - theta_bar)),
# and kappa is about 0.01-0.02 at the 16-line level, i.e. the basket shrinks a K fifty- to a hundredfold. The
# inverse model rescales it back to group-growth units (same t-statistic, honest units).
#
# Two theta sources:
#  (A) BLS distributional PCE (dPCE, March 2025 results) Table 1: decile shares of the 22 NIPA Table 2.3.5
#      major-product lines, 2000-2023; deciles of equivalized PCE (spending, not income). 16 leaf lines.
#  (B) CE Table 1110 (deciles of income before taxes, 2014-2025) leaf line items -> UCCs (BLS integrated
#      hierarchical-grouping files) -> PCE series (BLS ce_pce_map + a documented supplement for Diary UCCs the
#      map sources from the Interview) -> 2.4.5U lines. Allocation weights from BLS Table 2500 (detailed
#      all-CU means at UCC level).
#
# Run from the repo root:  venv/bin/python -I consumption/recent/code/fingerprint.py
# Outputs: consumption/recent/out/fingerprint_*.csv, out/top_tilt_monthly.csv, figures/fig_fingerprint_*.png,
# figures/fig_top_tilt.png. Checks: consumption/recent/checks/check_fingerprint.py.
# Plain functions plus top-level code, so each block can be pasted into a notebook cell.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                      # consumption/recent/code
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "code"))          # consumption/code (common.py)

import difflib
import re
import warnings
import zipfile

import numpy as np
import pandas as pd
from scipy import stats
from tqdm.auto import tqdm

import common

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

RECENT = HERE.parent
OUT = RECENT / "out"
FIG = RECENT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
TIDY = common.TIDY
RAW = common.RAW

SEED = 20261102
N_PERM = 1000
N_BOOT = 1000
ZANDI_TOP, ZANDI_B80 = 0.04, 0.0          # Zandi (EconoFact, 2026-07-24): top 20% ~4%/yr real, bottom 80% ~0
DEC = [f"d{k:02d}" for k in range(1, 11)]
GROUPS = {"top20": DEC[8:], "b80": DEC[:8],
          "q1": DEC[0:2], "q2": DEC[2:4], "q3": DEC[4:6], "q4": DEC[6:8], "q5": DEC[8:10],
          "b50": DEC[:5], "p50_80": DEC[5:8], "p80_90": ["d09"], "top10": ["d10"]}
SPEC_GROUPS = {"2grp": ["b80", "top20"], "4grp": ["b50", "p50_80", "p80_90", "top10"],
               "5grp": ["q1", "q2", "q3", "q4", "q5"]}
SPEC_TOP = {"2grp": ["top20"], "4grp": ["p80_90", "top10"], "5grp": ["q5"]}
CE_YEARS = list(range(2014, 2026))
DPCE_YEARS = list(range(2000, 2024))

# %% 1. NIPA tables as wide frames
# ---------------------------------------------------------------------------------------------------------
# 1. NIPA tables as wide frames: W[(table, freq)] -> index date ('YYYY' or 'YYYY-MM'), columns line
# ---------------------------------------------------------------------------------------------------------


def load_nipa():
    W = {}
    u = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", usecols=["table", "freq", "line", "date", "value"],
                    dtype={"table": str, "freq": str, "date": str})
    for (t, f), g in u.groupby(["table", "freq"]):
        W[(t, f)] = g.pivot(index="date", columns="line", values="value").sort_index()
    m = pd.read_csv(TIDY / "bea_pce_major_long.csv", usecols=["table", "freq", "line", "date", "value"],
                    dtype={"table": str, "freq": str, "date": str})
    for (t, f), g in m.groupby(["table", "freq"]):
        W[(t, f)] = g.pivot(index="date", columns="line", values="value").sort_index()
    return W


W = load_nipa()
ULINES = pd.read_csv(TIDY / "bea_pce_u_lines.csv", dtype={"code_2_4_5U": str, "path_lines": str, "context": str})
ULINES = ULINES.set_index("line")
UMAIN = ULINES[ULINES.section == "main"]
CODE2ULINE = {c: int(l) for l, c in UMAIN.code_2_4_5U.items()}           # BEA mnemonic -> 2.4.5U main line
ULABEL = UMAIN.label_short.to_dict()
UPATH = {int(l): [int(x) for x in p.split(">")] for l, p in UMAIN.path_lines.items()}
UCHILDREN = {}
for l, p in UPATH.items():
    if len(p) > 1:
        UCHILDREN.setdefault(p[-2], []).append(l)

MAJ = pd.read_csv(TIDY / "bea_pce_major_long.csv", usecols=["table", "line", "series_code", "label"],
                  dtype={"table": str}).drop_duplicates(["table", "line"])
MAJ235 = MAJ[MAJ.table == "2.3.5"].set_index("line")
MAJ285 = MAJ[MAJ.table == "2.8.5"].set_index("line")
A_CATS = [4, 5, 6, 7, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22]   # leaf major-product lines of 2.3.5
MAJ2U = {int(l): CODE2ULINE[MAJ235.at[l, "series_code"]] for l in A_CATS + [1]}
A_LABEL = {l: MAJ235.at[l, "label"] for l in A_CATS}
A_SHORT = {4: "Motor vehicles", 5: "Furnishings", 6: "Recreational goods", 7: "Other durables",
           9: "Food at home", 10: "Clothing", 11: "Gasoline & energy goods", 12: "Other nondurables",
           15: "Housing & utilities", 16: "Health care", 17: "Transport services", 18: "Recreation services",
           19: "Food services & hotels", 20: "Financial services & ins.", 21: "Other services", 22: "NPISHs"}
# line correspondence 2.3.5 <-> 2.8.5 (same series codes for lines 1-22): checked here, reported in checks
LINE_CORR_OK = all(MAJ235.at[l, "series_code"] == MAJ285.at[l, "series_code"] for l in range(1, 23))


def descendants(line):
    out, stack = [], [line]
    while stack:
        x = stack.pop()
        for c in UCHILDREN.get(x, []):
            out.append(c)
            stack.append(c)
    return out


def in_subtree(line, roots):
    return any(r in UPATH[line] for r in roots)


def nominal(kind, freq):
    """Current-dollar wide table: kind 'A' (major lines, 2.3.5 / 2.8.5) or 'U' (2.4.5U)."""
    if kind == "A":
        return W[("2.3.5", "A")] if freq == "A" else W[("2.8.5", "M")]
    return W[("2.4.5U", freq)]


def growth_frame(kind, lines, t0, t1, freq):
    """Nominal and real growth t0 -> t1 per category line. Real: chained dollars (2.3.6 / 2.8.6 / 2.4.6U)
    where both endpoints are published (2007 on), else the 2.4.3U quantity index of the same series."""
    nom = nominal(kind, freq)
    if kind == "A":
        ch = W[("2.3.6", "A")] if freq == "A" else W[("2.8.6", "M")]
        qline = {l: MAJ2U[l] for l in lines}
    else:
        ch = W[("2.4.6U", freq)]
        qline = {l: l for l in lines}
    qi = W[("2.4.3U", freq)]
    rows = []
    for l in lines:
        s0, s1 = nom.at[t0, l], nom.at[t1, l]
        c0 = ch.at[t0, l] if (t0 in ch.index and l in ch.columns) else np.nan
        c1 = ch.at[t1, l] if (t1 in ch.index and l in ch.columns) else np.nan
        if np.isfinite(c0) and np.isfinite(c1) and c0 > 0:
            gr, src = c1 / c0 - 1, "chained"
        else:
            q0, q1 = qi.at[t0, qline[l]], qi.at[t1, qline[l]]
            gr, src = q1 / q0 - 1, "quantity_index"
        rows.append(dict(line=l, S0=s0, S1=s1, g_nom=s1 / s0 - 1, g_real=gr, real_source=src))
    return pd.DataFrame(rows).set_index("line")


# %% 2. Source A
# ---------------------------------------------------------------------------------------------------------
# 2. Source A: BLS distributional PCE (dPCE), March 2025 vintage
# ---------------------------------------------------------------------------------------------------------
DP = pd.read_csv(TIDY / "bls_dpce_long.csv")
DP = DP[DP.vintage == "2025-03"]
_t1 = DP[DP.table == "T1"]
DP_SHARE = _t1[_t1.measure == "decile_share_of_category"].pivot_table(
    index=["year", "nipa_2_3_5_line"], columns="group", values="value")[DEC]
DP_PCE = _t1[_t1.measure == "pce"].pivot_table(index="year", columns="nipa_2_3_5_line", values="value")
_t3 = DP[(DP.table == "T3") & (DP.line.between(2, 11))]
DP_PRICE = _t3.pivot_table(index="year", columns="group", values="value")[DEC]   # 2017 = 100, decile indexes


def theta_A(year):
    """Decile market shares of the 16 leaf lines in dPCE year `year` (rows renormalized to sum to 1)."""
    t = DP_SHARE.loc[year].loc[A_CATS].astype(float)
    return t.div(t.sum(axis=1), axis=0)


def group_theta(theta_dec, groups):
    return pd.DataFrame({g: theta_dec[GROUPS[g]].sum(axis=1) for g in groups})


def dpce_group_spending(year):
    """Actual dPCE spending by decile (billions, nominal): published decile shares of line 1 x line-1 total."""
    return DP_SHARE.loc[(year, 1)].astype(float) * DP_PCE.at[year, 1]


def dpce_group_growth(y0, y1, groups, real=False):
    x0, x1 = dpce_group_spending(y0), dpce_group_spending(y1)
    if real:
        x0 = x0 / (DP_PRICE.loc[y0] / 100.0)
        x1 = x1 / (DP_PRICE.loc[y1] / 100.0)
    return {g: x1[GROUPS[g]].sum() / x0[GROUPS[g]].sum() - 1 for g in groups}


ALL_GROUPS = list(GROUPS)
rows = []
for y in DPCE_YEARS:
    th = theta_A(y)
    tg = group_theta(th, ALL_GROUPS)
    s_nipa = W[("2.3.5", "A")].loc[str(y), A_CATS]
    for l in A_CATS:
        r = dict(source="A_dPCE", base_year=y, category=l, category_label=A_LABEL[l],
                 base_spending_dpce_bn=float(DP_PCE.at[y, l]), base_spending_nipa_bn=float(s_nipa[l]) / 1000.0)
        r.update({f"theta_{d}": float(th.at[l, d]) for d in DEC})
        r.update({f"theta_{g}": float(tg.at[l, g]) for g in ALL_GROUPS})
        r["theta_row_sum"] = float(th.loc[l].sum())
        rows.append(r)
THETA_A = pd.DataFrame(rows)
THETA_A.to_csv(OUT / "fingerprint_theta_A.csv", index=False, float_format="%.10g")

# %% 3. Source B
# ---------------------------------------------------------------------------------------------------------
# 3. Source B: CE Table 1110 line items -> UCCs -> PCE lines
# ---------------------------------------------------------------------------------------------------------
# Vendored through common.fetch (skipped when present). BLS hosts get the approved contact User-Agent.
common.fetch("bls_ce", "stubs/pumd_doc.htm", "https://www.bls.gov/cex/pumd_doc.htm",
             "BLS CE Public-Use Microdata documentation page (lists the hierarchical grouping files)",
             "recent/fingerprint: locate the CE hierarchical grouping (stub) files")
common.fetch("bls_ce", "stubs/stubs.zip", "https://www.bls.gov/cex/pumd/stubs.zip",
             "BLS CE PUMD hierarchical groupings (stub files), integrated/interview/diary, 1996-2025",
             "recent/fingerprint: map CE Table 1110 line items to UCCs (then to PCE via ce_pce_map)")
for _y in CE_YEARS:
    common.fetch("bls_ce", f"tables/detail/cu-all-detail-{_y}.xlsx",
                 f"https://www.bls.gov/cex/tables/calendar-year/mean/cu-all-detail-{_y}.xlsx",
                 f"CE calendar-year table: all consumer units, detailed expenditure means, variances and percent "
                 f"reporting, {_y} (near-UCC detail)",
                 "recent/fingerprint: spending weights to allocate Table 1110 line items across PCE lines (UCC level)")

STUB_ZIP = RAW / "bls_ce" / "stubs" / "stubs.zip"
STUB_PAT = re.compile(r"^\s*(\S+)\s+(?:[-A-Z]\s+)?([A-Z])\s+(-?\d+)\s+(\S+)\s*$")

# Supplement to BLS's ce_pce_map: UCCs that the published integrated tables take from the Diary (or that are
# newer than the map) while the map sources the same spending from Interview UCCs. Judgment table; each target
# follows BLS's own target for the analogous UCC. (ucc -> (BEA mnemonic, reason))
_FOOD_AWAY = ["190111", "190112", "190113", "190114", "190211", "190212", "190213", "190214", "190311", "190312",
              "190313", "190314", "190321", "190322", "190323", "190324", "190400", "190500", "190600", "190700"]
_ALC_AWAY = [f"2005{a}{b}" for a in "123" for b in "123456"]
SUPP_MAP = {u: ("DOPMRC", "Diary food-away UCC; BLS map sources purchased meals from Interview 790410/790400 (DOPMRC)")
            for u in _FOOD_AWAY}
SUPP_MAP.update({u: ("DAPMRC", "Diary alcohol-away UCC; BLS map sources it from Interview 790420/200900 (DAPMRC)")
                 for u in _ALC_AWAY})
SUPP_MAP.update({
    "310312": ("DVAARC", "Diary audio equipment; same PCE line as BLS's Interview AV equipment UCCs"),
    "310315": ("DVAARC", "Diary video players; as above"),
    "310331": ("DVAARC", "Diary sound equipment; as above"),
    "310332": ("DVAARC", "Diary sound accessories; as above"),
    "310335": ("DVAARC", "Diary video equipment; as above"),
    "480215": ("DVAARC", "vehicle video equipment (to 2013Q1)"),
    "620912": ("DAVPRC", "rental of video media; BLS sends rental of video software 620918 to DAVPRC"),
    "590110": ("DMAGRC", "Diary newspapers; BLS map sources newspapers from Interview 590310/590410 (DMAGRC)"),
    "590210": ("DMAGRC", "Diary magazines; BLS map sources magazines from Interview 590310/590410 (DMAGRC)"),
    "370901": ("DMBCRC", "boys' uniforms and sportswear; BLS sends boys' apparel to DMBCRC"),
    "660000": ("DSTYRC", "school supplies, unspecified (Diary); BLS splits school supplies to DSTYRC/DEBKRC"),
    "280230": ("DSEWRC", "sewing materials for the home; BLS sends sewing items to DSEWRC"),
    "490000": ("DVMRRC", "misc. auto repair (Diary); BLS sends vehicle repair to DVMRRC"),
    "300900": ("DSEARC", "misc. household appliances (Diary)"),
    "570902": ("DOMORC", "repair of medical equipment; BLS sends rental of medical equipment 570901 to DOMORC"),
    "550350": ("DOMPRC", "purchase/rental of convalescent equipment (2024 UCC); BLS sends 550330 to DOMPRC"),
    "680903": ("DPCSRC", "misc. personal services (Diary); BLS sends dating/personal services to DPCSRC"),
    "790915": ("DFEERC", "late fee on mortgage (2024 UCC); financial service charge"),
    "830111": ("DFEERC", "late fee on mortgage (2024 UCC); financial service charge"),
    "830112": ("DFEERC", "late fee on mortgage (2024 UCC); financial service charge"),
    "180230": ("DOFDRC", "frozen meals (2025 UCC); BLS sends frozen prepared foods to DOFDRC"),
    "180720": ("DNRDRC", "vitamin supplements (Diary); BLS sends vitamins 550410/550219 to DNRDRC"),
    "320140": ("DTOORC", "laundry and cleaning equipment (Diary)"),
    "320430": ("DTOORC", "other hardware (Diary); BLS sends hardware to DTOORC"),
    "320905": ("DTOORC", "misc. household equipment and parts (Diary)"),
    "690115": ("DIPERC", "personal digital assistants (to 2013Q1)"),
    "690210": ("DTCERC", "telephone answering devices (to 2013Q1)"),
    "690241": ("DTOORC", "smoke alarms (to 2013Q1)"), "690242": ("DTOORC", "smoke alarms (to 2013Q1)"),
    "690243": ("DTOORC", "smoke alarms (to 2013Q1)"),
    "600133": ("DBARRC", "purchase of boats and trailers (2024 UCC); BLS sends 600132/600121 to DBARRC"),
    "600151": ("DBARRC", "purchase of motor homes and campers (2024 UCC); BLS sends 600141 to DBARRC"),
    "620910": ("DRLSRC", "rental of boats and trailers (2024 UCC); BLS sends rental of boat 620906 to DRLSRC"),
    "620924": ("DMVRRC", "rental of RVs and other vehicles (2024 UCC); BLS sends 620921/620922 to DMVRRC"),
    "340421": ("DMHSRC", "water softening (2024 UCC); BLS sends 340420 to DMHSRC"),
    "340422": ("DMHSRC", "water softening (2024 UCC); BLS sends 340420 to DMHSRC"),
    "270906": ("DMHSRC", "septic tank cleaning (2024 UCC); BLS sends 270901-270904 to DMHSRC"),
    "270907": ("DMHSRC", "septic tank cleaning (2024 UCC); BLS sends 270901-270904 to DMHSRC"),
    "340913": ("DFRERC", "repair of misc. household equipment and furnishings (Diary)"),
    "320380": ("DNECRC", "tableware and nonelectric kitchenware (Diary)"),
})
# UCCs inside Table 1110 expenditure items that are not PCE by NIPA concept (left out on purpose).
OUT_OF_SCOPE_PREFIX = {
    "8001": "cash contribution / transfer (not PCE)", "8008": "cash contribution / transfer (not PCE)",
    "8009": "pension or Social Security contribution (saving / social insurance, not PCE)",
}
OUT_OF_SCOPE = {
    "220211": "property tax (tax, not PCE)", "220212": "property tax on vacation home (tax, not PCE)",
    "950021": "other taxes (not PCE)", "950024": "vehicle personal property tax (not PCE)",
    "510115": "vehicle registration incl. property tax (government fee, not PCE)",
    "520110": "vehicle registration (government fee, not PCE)", "520111": "vehicle registration (government fee)",
    "520112": "vehicle registration (government fee)", "520310": "driver's license (government fee, not PCE)",
    "220311": "mortgage interest (personal interest payment, not PCE)",
    "220312": "mortgage interest, vacation home (not PCE)",
    "580901": "Medicare premium (contribution for government social insurance, not PCE)",
    "580907": "Medicare drug premium (social insurance contribution, not PCE)",
    "580908": "Medicaid premium (government program, not PCE)", "580909": "Tricare premium (government program)",
    "580910": "CHIP premium (government program, not PCE)",
    "920050": "educational savings account (saving, not PCE)", "671000": "prepaid tuition (prepayment/saving)",
}
_OWNER_MAINT = {"210901", "210902", "230112", "230113", "230114", "230115", "230122", "230123", "230142", "230143",
                "230151", "240112", "240122", "240212", "240213", "240222", "240312", "240322", "320612", "320622",
                "320623", "320625", "320632", "990930"}
_RENTER_MAINT = {"230121", "230141", "230144", "230150", "240111", "240121", "240211", "240311", "240321", "320611",
                 "320621", "320624", "320631", "790690", "990920"}
for _u in _OWNER_MAINT:
    OUT_OF_SCOPE[_u] = "owner-occupied housing maintenance / ground rent (input to imputed rent, not PCE)"
for _u in _RENTER_MAINT:
    OUT_OF_SCOPE[_u] = "renter-paid dwelling maintenance (left out of BLS's map; housing-services input)"


def norm_name(s):
    s = str(s)
    s = re.sub(r"\[[ID]\]", "", s)
    s = re.sub(r"\((new UCC|through|thru)[^)]*\)", "", s)
    s = re.sub(r"\(new title[^)]*\)", "", s)
    s = s.replace("''", "'").replace("’", "'")
    s = re.sub(r"\s+", " ", s).strip().lower()
    s = re.sub(r"\s+[a-e]/$", "", s)
    return s.rstrip(":").strip()


def parse_stub(zf, year):
    text = zf.read(f"stubs/CE-HG-Integ-{year}.txt").decode("latin-1")
    rows = []
    for line in text.splitlines():
        if not line.strip() or line[0] == "*":
            continue
        if line[0] == "2":
            rows[-1]["name"] += " " + line[6:69].strip()
            continue
        m = STUB_PAT.match(line[69:])
        rows.append(dict(level=int(line[3]), name=line[6:69].strip(), code=m.group(1), src=m.group(2),
                         factor=int(m.group(3)), section=m.group(4)))
    st = pd.DataFrame(rows)
    i0 = int(st.index[st.code.str.startswith("TOTALE")][0])
    lev0 = st.level[i0]
    end = i0 + 1
    while end < len(st) and st.level[end] > lev0:
        end += 1
    sub = st.iloc[i0:end].reset_index(drop=True)
    sub["nname"] = sub["name"].map(norm_name)
    path, paths = [], []
    for _, r in sub.iterrows():
        path = path[: r.level - lev0] + [r.nname]
        paths.append(" > ".join(path))
    sub["npath"] = paths
    return sub, st


def stub_uccs(sub, i):
    """UCC rows (Interview or Diary source) at or below stub row i."""
    out = []
    if sub.src[i] in ("I", "D"):
        out.append(i)
    for j in range(i + 1, len(sub)):
        if sub.level[j] <= sub.level[i]:
            break
        if sub.src[j] in ("I", "D"):
            out.append(j)
    return out


def parse_detail(year):
    """Table 2500 (all CUs, detailed means): (label, mean, code kind) for the expenditure block, in sheet
    order. Codes are read through that year's own legend (letters change meaning across years)."""
    import openpyxl
    wb = openpyxl.load_workbook(RAW / "bls_ce" / "tables" / "detail" / f"cu-all-detail-{year}.xlsx", read_only=False)
    ws = wb[wb.sheetnames[0]]
    legend = {}
    for r in ws.iter_rows(min_row=max(1, ws.max_row - 40)):
        m = re.match(r"^([a-e])\s+(.*)$", str(r[0].value or "").strip())
        if m:
            txt = m.group(2).lower()
            legend[m.group(1) + "/"] = ("suppressed" if "suppressed" in txt else "too_small" if "too small" in txt
                                        else "no_data" if "no data" in txt else "other")
    items, cur = [], None
    for r in ws.iter_rows(min_row=1):
        lab, val = r[0].value, r[1].value
        if lab is None or str(lab).strip() == "":
            continue
        lab = str(lab).strip()
        if lab.lower() in ("mean", "share", "se", "rse", "percent reporting", "cv(%)"):
            if cur is not None and lab.lower() == "mean":
                if isinstance(val, (int, float)):
                    cur["mean"], cur["code"] = float(val), ""
                else:
                    kind = legend.get(str(val).strip(), "other")
                    cur["mean"], cur["code"] = (0.0 if kind in ("too_small", "no_data") else np.nan), kind
            continue
        cur = dict(label=lab, mean=np.nan, code="")
        items.append(cur)
    j0 = [k for k, it in enumerate(items) if it["label"].startswith("Average annual expenditures")][0]
    return items[j0:]


def align_detail(sub, det):
    """Map stub rows to Table 2500 rows with difflib opcodes on normalized titles (equal blocks, then
    equal-length replace blocks pairwise, then fuzzy pairs inside other blocks).
    Returns {stub_row: (mean, code_kind)}."""
    a = list(sub.nname)
    b = [norm_name(d["label"]) for d in det]
    out = {}
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                out[i1 + k] = (det[j1 + k]["mean"], det[j1 + k]["code"])
        elif tag == "replace":
            if i2 - i1 == j2 - j1:
                for k in range(i2 - i1):
                    if difflib.SequenceMatcher(None, a[i1 + k], b[j1 + k]).ratio() > 0.6:
                        out[i1 + k] = (det[j1 + k]["mean"], det[j1 + k]["code"])
            else:
                for i in range(i1, i2):
                    best = max(range(j1, j2), key=lambda j: difflib.SequenceMatcher(None, a[i], b[j]).ratio())
                    if difflib.SequenceMatcher(None, a[i], b[best]).ratio() > 0.85:
                        out[i] = (det[best]["mean"], det[best]["code"])
    return out


CEMAP = pd.read_csv(TIDY / "ce_pce_map.csv", dtype=str)
CEMAP["pline"] = CEMAP.pce_series.map(CODE2ULINE)
assert CEMAP.pline.notna().all()
UCC2SERIES = CEMAP.groupby("ucc").pce_series.apply(lambda s: sorted(set(s))).to_dict()
UCC_TITLE_MAP = CEMAP.drop_duplicates("ucc").set_index("ucc").ucc_title.to_dict()
CE = pd.read_csv(TIDY / "ce_income_deciles_long.csv")
CE_EXP = CE[CE.path.str.startswith("Average annual expenditures") & (CE.stat == "mean")]


def ce_counts(year):
    x = CE[(CE.year == year) & (CE.path == "Number of consumer units (in thousands)")]
    s = x.set_index("group").value
    return s[DEC].astype(float), float(s["all"])


def ce_item_table(year):
    """Decile means for every expenditure path of `year` (columns d01..d10, all), with flags."""
    x = CE_EXP[CE_EXP.year == year]
    t = x.pivot_table(index="path", columns="group", values="value", aggfunc="first")
    meta = x.drop_duplicates("path").set_index("path")[["item_clean", "parent_item", "is_leaf", "depth"]]
    return t.reindex(columns=DEC + ["all"]), meta


def fill_item(vals, N, Nall):
    """Fill suppressed decile means from the all-CU identity N_all*m_all = sum_d N_d*m_d; the residual is
    spread over the missing deciles equally per CU. Returns (filled series, n_filled, filled share)."""
    v = vals.copy()
    miss = [d for d in DEC if not np.isfinite(v[d])]
    if not miss:
        return v, 0, 0.0
    tot = Nall * v["all"]
    shown = sum(N[d] * v[d] for d in DEC if d not in miss)
    resid = max(tot - shown, 0.0)
    for d in miss:
        v[d] = resid / sum(N[m] for m in miss)
    return v, len(miss), resid / tot if tot > 0 else np.nan


def build_items(year):
    """Table 1110 items used for B in `year`: leaves, with the partial-parent fixes and the owner rental
    equivalence addendum. Returns DataFrame indexed by item key with decile means (filled) and stub node."""
    t, meta = ce_item_table(year)
    N, Nall = ce_counts(year)
    leaves = [p for p in t.index if bool(meta.at[p, "is_leaf"])]
    items = {}
    gas_parent = "Average annual expenditures > Transportation > Gasoline and other fuels"
    veh_parent = "Average annual expenditures > Transportation > Vehicle purchases (net outlay)"
    for p in leaves:
        if p.startswith(gas_parent + " > "):           # 2023-2025: only 'Gasoline' shown; use the parent
            continue
        if not np.isfinite(t.loc[p, "all"]):            # all-CU missing: parent minus shown siblings
            par = p.rsplit(" > ", 1)[0]
            sib = [s for s in t.index if s.startswith(par + " > ") and s.count(" > ") == p.count(" > ") and s != p]
            v = t.loc[par, "all"] - np.nansum([t.loc[s, "all"] for s in sib])
            t.loc[p, "all"] = max(v, 0.0)
        items[p] = t.loc[p].copy()
    if gas_parent in t.index:
        items[gas_parent] = t.loc[gas_parent].copy()
    veh_kids = [s for s in leaves if s.startswith(veh_parent + " > ")]
    if veh_parent in t.index and not any(s.endswith("Other vehicles") for s in veh_kids):   # 2024-2025
        r = t.loc[veh_parent] - sum(t.loc[s] for s in veh_kids)
        items[veh_parent + " > Other vehicles (residual)"] = r.clip(lower=0.0)
    # owner rental equivalence (Addenda, monthly, non-owners count as zero) -> annual
    x = CE[(CE.year == year) & (CE.stat == "mean") & CE.item_clean.str.contains("monthly rental value of owned home",
                                                                                  case=False, regex=False)]
    rv = x.set_index("group").value.reindex(DEC + ["all"]).astype(float) * 12.0
    items["Addenda > Estimated monthly rental value of owned home (x12)"] = rv
    rows = []
    for k, v in items.items():
        vf, nf, fs = fill_item(v, N, Nall)
        agg = {d: N[d] * vf[d] for d in DEC}            # thousands of CUs x $ = $ thousands
        tot = sum(agg.values())
        r = dict(item_key=k, item=k.split(" > ")[-1], mean_all=float(vf["all"]), n_filled=nf, filled_share=fs,
                 agg_total_k=tot)
        r.update({f"theta_{d}": (agg[d] / tot if tot > 0 else np.nan) for d in DEC})
        r.update({f"mean_{d}": float(vf[d]) for d in DEC})
        rows.append(r)
    return pd.DataFrame(rows).set_index("item_key")


ALIAS_CODE = {"gasoline, other fuels, and motor oil": ["GASOIL"], "gasoline and motor oil": ["GASOIL"],
              "gasoline and other fuels": ["GASFUEL", "GASOIL"], "other vehicles (residual)": ["OTHVEHCL", "OTHVEH"]}


def match_item_nodes(item_key, sub):
    """Stub rows whose UCCs make up a Table 1110 item."""
    name = norm_name(item_key.split(" > ")[-1])
    if name in ALIAS_CODE:
        rows = [int(i) for c in ALIAS_CODE[name] for i in sub.index[sub.code == c]]
        if rows:
            return rows, "alias_code"
    target = " > ".join(norm_name(p) for p in item_key.split(" > "))
    hit = list(sub.index[sub.npath == target])
    if len(hit) == 1:
        return hit, "path"
    hit = list(sub.index[sub.nname == name])
    if len(hit) > 1:                                  # e.g. 'Fats and oils' group and UCC: take the group row
        hit = [min(hit, key=lambda i: sub.level[i])]
    if len(hit) == 1:
        return hit, "name"
    return [], "unmatched"


def nearest_ucc_mean(ucc, year):
    """All-CU mean of a UCC from the nearest other CE year that publishes it (ties: the later year)."""
    for z in sorted((z for z in CE_YEARS if z != year), key=lambda z: (abs(z - year), -z)):
        if ucc in UCC_MEANS.get(z, {}):
            return UCC_MEANS[z][ucc], z
    return np.nan, None


def map_year(year):
    """Item -> UCC -> PCE-line links for CE year `year`, with Table 2500 spending weights. A UCC mean that
    Table 2500 suppresses (2022-2023: RSE >= 25%) or that could not be aligned is taken from the nearest
    year that publishes it; 'too small' and 'no data reported' count as zero."""
    sub, dm = STUBS[year], DMEAN[year]
    items = build_items(year)
    links = []
    for key in items.index:
        if key.startswith("Addenda > "):
            ucc_rows = [("910050", "Estimated monthly rental value of owned home", "I", items.at[key, "mean_all"], "")]
            how = "addendum"
        else:
            nodes, how = match_item_nodes(key, sub)
            ucc_rows = []
            for n in nodes:
                for j in stub_uccs(sub, n):
                    mu, code = dm.get(j, (np.nan, "unaligned"))
                    ucc_rows.append((sub.code[j], sub["name"][j], sub.src[j], mu, code))
        if not ucc_rows:
            links.append(dict(year=year, item_key=key, match=how, ucc=None, map_source="no_ucc"))
            continue
        for ucc, title, src, mu, code in ucc_rows:
            from_year = year
            if not np.isfinite(mu):
                mu, from_year = nearest_ucc_mean(ucc, year)
            base = dict(year=year, item_key=key, item=items.at[key, "item"], match=how, ucc=ucc, ucc_title=title,
                        ucc_survey=src, ucc_mean_all=mu, ucc_mean_code=code, ucc_mean_from_year=from_year)
            if ucc in UCC2SERIES:
                for s in UCC2SERIES[ucc]:
                    links.append(dict(base, map_source="BLS_ce_pce_map", pce_series=s, pce_line=CODE2ULINE[s],
                                      n_targets=len(UCC2SERIES[ucc]), reason=""))
            elif ucc in SUPP_MAP:
                s, why = SUPP_MAP[ucc]
                links.append(dict(base, map_source="supplement", pce_series=s, pce_line=CODE2ULINE[s],
                                  n_targets=1, reason=why))
            else:
                why = OUT_OF_SCOPE.get(ucc) or next((v for k, v in OUT_OF_SCOPE_PREFIX.items() if ucc.startswith(k)),
                                                    None)
                links.append(dict(base, map_source="out_of_scope" if why else "unmapped", pce_series=None,
                                  pce_line=np.nan, n_targets=0, reason=why or "no PCE target in BLS map; dropped"))
    return items, pd.DataFrame(links)


def categories_from_links(lk, year):
    """B categories: the lowest mapped 2.4.5U lines (a mapped line with no mapped descendant; its subtree is
    collapsed). A mapped line that has mapped descendants passes its weight down to them by PCE size."""
    S = W[("2.4.5U", "A")].loc[str(year)]
    mapped = set(int(x) for x in lk.pce_line.dropna().unique())
    cats = sorted(l for l in mapped if not any(d in mapped for d in descendants(l)))
    spread = {}
    for l in mapped - set(cats):
        kids = [c for c in cats if l in UPATH[c]]
        tot = sum(S[c] for c in kids)
        spread[l] = {c: S[c] / tot for c in kids}
    return cats, spread


def build_B(year):
    items, lk = map_year(year)
    S = W[("2.4.5U", "A")].loc[str(year)]
    m = lk[lk.pce_line.notna()].copy()
    m["pce_line"] = m.pce_line.astype(int)
    # split share of a UCC across its BLS targets: in proportion to the targets' PCE values in `year`
    tsum = m.groupby(["item_key", "ucc"]).pce_line.transform(lambda s: sum(S[x] for x in s))
    m["split_share"] = m.pce_line.map(lambda x: S[x]) / tsum
    m["ucc_weight"] = m.ucc_mean_all.clip(lower=0).fillna(0.0) * m.split_share
    cats, spread = categories_from_links(m, year)
    rows = []
    for _, r in m.iterrows():
        if r.pce_line in spread:
            for c, sh in spread[r.pce_line].items():
                rows.append(dict(r, category=c, weight=r.ucc_weight * sh, rule="spread_to_mapped_descendants"))
        else:
            rows.append(dict(r, category=r.pce_line, weight=r.ucc_weight, rule="direct"))
    cl = pd.DataFrame(rows)
    # item -> category weights E_ic; fallback to equal weights if a category's feeders all carry zero weight
    E = cl.groupby(["category", "item_key"]).weight.sum().reset_index()
    zero = E.groupby("category").weight.transform("sum") <= 0
    E.loc[zero, "weight"] = 1.0
    th = items[[f"theta_{d}" for d in DEC]]
    out = []
    for c, g in E.groupby("category"):
        w = g.set_index("item_key").weight
        tc = (th.loc[w.index].mul(w, axis=0).sum() / w.sum()).values
        r = dict(source="B_CE", base_year=year, category=int(c), category_label=ULABEL[int(c)],
                 base_spending_nipa_bn=float(S[c]) / 1000.0, ce_weight_per_cu=float(w.sum()),
                 n_items=len(w), items=" | ".join(sorted(k.split(" > ")[-1] for k in w.index)),
                 equal_weight_fallback=bool(zero[g.index].any()))
        r.update({f"theta_{d}": float(tc[i]) for i, d in enumerate(DEC)})
        out.append(r)
    thB = pd.DataFrame(out)
    tg = group_theta(thB.set_index("category")[[f"theta_{d}" for d in DEC]].rename(columns=lambda s: s[6:]),
                     ALL_GROUPS)
    for g in ALL_GROUPS:
        thB[f"theta_{g}"] = thB.category.map(tg[g])
    thB["theta_row_sum"] = thB[[f"theta_{d}" for d in DEC]].sum(axis=1)
    cl["pce_line"] = cl.pce_line.astype(float)
    lk = lk.merge(cl[["item_key", "ucc", "pce_line", "category", "split_share", "weight", "rule"]],
                  on=["item_key", "ucc", "pce_line"], how="left")
    return items, lk, thB, cats


ZF = zipfile.ZipFile(STUB_ZIP)
STUBS, DMEAN, UCC_MEANS = {}, {}, {}
for y in tqdm(CE_YEARS, desc="CE stubs + Table 2500 alignment"):
    STUBS[y], _ = parse_stub(ZF, y)
    DMEAN[y] = align_detail(STUBS[y], parse_detail(y))
    UCC_MEANS[y] = {STUBS[y].code[j]: v[0] for j, v in DMEAN[y].items()
                    if STUBS[y].src[j] in ("I", "D") and np.isfinite(v[0])}
B_ITEMS, B_LINKS, B_THETA, B_CATS = {}, {}, {}, {}
for y in tqdm(CE_YEARS, desc="source B mapping by CE year"):
    B_ITEMS[y], B_LINKS[y], B_THETA[y], B_CATS[y] = build_B(y)

pd.concat([B_THETA[y] for y in CE_YEARS], ignore_index=True).to_csv(OUT / "fingerprint_theta_B.csv", index=False,
                                                                     float_format="%.10g")
_mcols = ["year", "item_key", "item", "match", "ucc", "ucc_title", "ucc_survey", "ucc_mean_all", "ucc_mean_code",
          "ucc_mean_from_year", "map_source", "pce_series", "pce_line", "n_targets", "split_share", "category",
          "weight", "rule", "reason"]
MAPPING_B = pd.concat([B_LINKS[y] for y in CE_YEARS], ignore_index=True).reindex(columns=_mcols)
MAPPING_B["pce_label"] = MAPPING_B.pce_line.map(lambda l: ULABEL.get(int(l), "") if np.isfinite(l) else "")
MAPPING_B["category_label"] = MAPPING_B.category.map(lambda l: ULABEL.get(int(l), "") if np.isfinite(l) else "")
MAPPING_B["rule"] = MAPPING_B.rule.fillna("").replace({
    "direct": "item theta applies to the UCC's PCE line; a line fed by several items takes the mix of their thetas "
              "weighted by Table 2500 UCC means x split share (split UCCs divided by the targets' PCE values)",
    "spread_to_mapped_descendants": "UCC targets a non-leaf line whose sub-lines are mapped: weight spread over "
                                    "those sub-lines by their PCE values"})
MAPPING_B.to_csv(OUT / "fingerprint_mapping_B.csv", index=False, float_format="%.10g")


def uncovered_lines(year):
    """Highest main-hierarchy lines with no B category at or below or above them (no CE counterpart)."""
    S = W[("2.4.5U", "A")].loc[str(year)]
    cats = set(B_CATS[year])
    covered = set(cats) | {d for c in cats for d in descendants(c)} | {a for c in cats for a in UPATH[c]}
    out = []
    for l in UMAIN.index:
        l = int(l)
        if l in covered:
            continue
        par = UPATH[l][-2] if len(UPATH[l]) > 1 else None
        if par is not None and par not in covered:
            continue                                   # report only the highest uncovered line
        out.append(dict(line=l, label=ULABEL[l], sign_to_root=int(UMAIN.at[l, "sign_to_root"]),
                        value_bn=int(UMAIN.at[l, "sign_to_root"]) * float(S[l]) / 1000.0))
    return pd.DataFrame(out)


cov_rows = []
for y in CE_YEARS:
    S = W[("2.4.5U", "A")].loc[str(y)]
    th = B_THETA[y]
    health = [c for c in th.category if in_subtree(c, [172, 121, 66, 275])]
    lk = B_LINKS[y]
    it = B_ITEMS[y]
    exp_items = [k for k in it.index if not k.startswith("Addenda")]
    mapped_w = (lk[lk.pce_line.notna() & ~lk.item_key.str.startswith("Addenda")]
                .drop_duplicates(["item_key", "ucc"]).ucc_mean_all.clip(lower=0).sum())
    t, _ = ce_item_table(y)
    unc = uncovered_lines(y)
    cov_rows.append(dict(
        year=y, n_categories=len(th), pce_total_bn=float(S[1]) / 1000.0,
        pce_covered_bn=float(th.base_spending_nipa_bn.sum()),
        pce_covered_share=float(th.base_spending_nipa_bn.sum() * 1000.0 / S[1]),
        pce_covered_share_ex_health=float(th[~th.category.isin(health)].base_spending_nipa_bn.sum() * 1000.0 / S[1]),
        health_lines_bn=float(th[th.category.isin(health)].base_spending_nipa_bn.sum()),
        owner_rent_bn=float(th[th.category == 160].base_spending_nipa_bn.sum()),
        ce_spending_mapped_share=float(mapped_w / t.loc["Average annual expenditures", "all"]),
        n_ucc_supplement=int((lk.map_source == "supplement").sum()),
        n_ucc_out_of_scope=int(lk[lk.map_source == "out_of_scope"].ucc.nunique()),
        n_ucc_unmapped=int(lk[lk.map_source == "unmapped"].ucc.nunique()),
        n_items_filled=int((it.n_filled > 0).sum()),
        uncovered=" | ".join(f"{r.line} {r.label} {r.value_bn:+.0f}bn" for _, r in unc.iterrows())))
COVERAGE_B = pd.DataFrame(cov_rows)
COVERAGE_B.to_csv(OUT / "fingerprint_coverage_B.csv", index=False, float_format="%.10g")

# %% 4. Estimators
# ---------------------------------------------------------------------------------------------------------
# 4. Estimators
# ---------------------------------------------------------------------------------------------------------
RNG = np.random.default_rng(SEED)


def wmean(x, w):
    return float(np.sum(w * x) / np.sum(w))


def wls_line(y, x, w):
    """Weighted least squares of y on [1, x]: (intercept, slope)."""
    w = w / w.sum()
    xm, ym = np.sum(w * x), np.sum(w * y)
    b = np.sum(w * (x - xm) * (y - ym)) / np.sum(w * (x - xm) ** 2)
    return ym - b * xm, b


def batch_slopes(y, X, w):
    """Slopes of y on each row of X (shape n_rep x n), weighted; vectorized."""
    w = w / w.sum()
    xm = X @ w
    ym = np.sum(w * y)
    Xc = X - xm[:, None]
    return (Xc * (w * (y - ym))).sum(axis=1) / ((Xc ** 2) * w).sum(axis=1)


def kappa(theta, w):
    """Basket attenuation: basket gap = kappa x slope (two groups, same weights)."""
    tb = wmean(theta, w)
    return wmean((theta - tb) ** 2, w) / (tb * (1 - tb))


def fit_2grp(g, th, w, gap_z, perms):
    """Main two-group fit with classical and HC3 SEs, the permutation (placebo) null, and a permutation CI by
    test inversion: H0 gap = c is tested by permuting theta in g - c*theta (exact, linear in c)."""
    n = len(g)
    a, b = wls_line(g, th, w)
    res = g - a - b * th
    wn = w / w.mean()
    xm = np.sum(wn * th) / wn.sum()
    sxx = np.sum(wn * (th - xm) ** 2)
    s2 = np.sum(wn * res ** 2) / (n - 2)
    se = float(np.sqrt(s2 / sxx))
    # HC3 for the WLS slope (sandwich with leverage-adjusted squared residuals)
    X = np.column_stack([np.ones(n), th])
    XtWX_inv = np.linalg.inv(X.T @ (wn[:, None] * X))
    h = np.einsum("ij,jk,ik->i", X, XtWX_inv, X) * wn
    meat = (X * (wn * res / (1 - h))[:, None]).T @ (X * (wn * res / (1 - h))[:, None])
    se_hc3 = float(np.sqrt((XtWX_inv @ meat @ XtWX_inv)[1, 1]))
    tcrit = stats.t.ppf(0.975, n - 2)
    TH = th[perms]
    a_p = batch_slopes(g, TH, w)
    b_p = batch_slopes(th, TH, w)

    def p_at(c):
        return (1 + np.sum(np.abs(a_p - c * b_p) >= np.abs(b - c) - 1e-12)) / (len(perms) + 1)

    span = 8 * max(se, np.std(a_p), 1e-6)
    grid = np.linspace(b - span, b + span, 4001)
    obs = np.abs(b - grid)
    pg = (1 + (np.abs(a_p[None, :] - grid[:, None] * b_p[None, :]) >= obs[:, None] - 1e-12).sum(axis=1)) / (len(perms) + 1)
    acc = grid[pg > 0.05]
    tb = wmean(th, w)
    G = wmean(g, w)
    ssr = lambda pred: float(np.sum(w * (g - pred) ** 2) / np.sum(w))
    pred_fit = a + b * th
    pred_z = G + (th - tb) * gap_z
    pred_flat = np.full(n, G)
    return dict(n=n, x_b80=a, x_top20=a + b, gap=b, se=se, se_hc3=se_hc3,
                ci_t_lo=b - tcrit * se, ci_t_hi=b + tcrit * se,
                ci_perm_lo=float(acc.min()) if len(acc) else np.nan, ci_perm_hi=float(acc.max()) if len(acc) else np.nan,
                ci_perm_at_edge=bool(len(acc) and (acc.min() <= grid[0] or acc.max() >= grid[-1])),
                p_placebo=p_at(0.0), p_zandi=p_at(gap_z), perm_sd=float(np.std(a_p)),
                agg_growth=G, theta_bar=tb, kappa=kappa(th, w), basket_gap=kappa(th, w) * b,
                wrmse_fit=np.sqrt(ssr(pred_fit)), wrmse_zandi=np.sqrt(ssr(pred_z)), wrmse_flat=np.sqrt(ssr(pred_flat)),
                r2_fit_vs_flat=1 - ssr(pred_fit) / ssr(pred_flat), r2_zandi_vs_flat=1 - ssr(pred_z) / ssr(pred_flat),
                mde80=(tcrit + stats.norm.ppf(0.8)) * se)


def penalty_matrix(pi):
    K = len(pi)
    D = np.eye(K) - np.outer(np.ones(K), pi)
    return D.T @ np.diag(pi) @ D


LAMBDA_GRID = np.concatenate([[0.0], np.logspace(-7, 1, 33)])
N_RIDGE_REP = 500          # bootstrap and permutation replicates for the multi-group specs (lambda re-selected)


def loo_lambda(g, TH, wn, P, grid=LAMBDA_GRID):
    """Leave-one-category-out CV over `grid`, exact closed form for penalized WLS with the penalty held fixed:
    LOO residual_i = e_i / (1 - h_ii), h_ii = wn_i * TH_i (TH'W TH + lam P)^-1 TH_i'. wn sums to one."""
    A = TH.T @ (wn[:, None] * TH)
    rhs = TH.T @ (wn * g)
    cv = np.empty(len(grid))
    for k, lam in enumerate(grid):
        M = np.linalg.pinv(A) if lam == 0 else np.linalg.inv(A + lam * P)
        e = g - TH @ (M @ rhs)
        h = wn * np.einsum("ij,jk,ik->i", TH, M, TH)
        with np.errstate(divide="ignore", invalid="ignore"):
            cv[k] = np.sum(wn * (e / (1 - h)) ** 2) if np.all(h < 1 - 1e-9) else np.inf
    k = int(np.argmin(cv))
    return float(grid[k]), k == len(grid) - 1, cv


def ridge_fit(g, TH, wn, P, lam):
    A = TH.T @ (wn[:, None] * TH)
    rhs = TH.T @ (wn * g)
    if lam == 0:
        return np.linalg.lstsq(A, rhs, rcond=None)[0]
    return np.linalg.solve(A + lam * P, rhs)


def solve_groups(g, TH, w, lam, P):
    """Ridge toward equal growth: min sum_g wn (g - TH x)^2 + lam * sum_k pi_k (x_k - xbar_pi)^2 (wn = w / sum w).
    lam = 0 is unconstrained WLS (least-squares solution if singular)."""
    return ridge_fit(g, TH, w / w.sum(), P, lam)


def implied_gap(x, pi, groups, top):
    it = [i for i, gname in enumerate(groups) if gname in top]
    ib = [i for i, gname in enumerate(groups) if gname not in top]
    xt = np.sum(pi[it] * x[it]) / np.sum(pi[it])
    xb = np.sum(pi[ib] * x[ib]) / np.sum(pi[ib])
    return xt, xb, xt - xb


def fit_groups(g, TH, w, groups, top, perms, boots, lam=None):
    """Multi-group fit. Ridge (lam=None): lambda by exact LOO-CV, and re-selected inside every bootstrap and
    permutation replicate, so the interval and the placebo carry the lambda-selection uncertainty. OLS: lam=0.
    gap = spending-weighted top20 growth minus bottom80 growth (pi = groups' base spending shares)."""
    wn = w / w.sum()
    pi = TH.T @ wn
    P = penalty_matrix(pi)
    ridge = lam is None
    at_max = False
    if ridge:
        lam, at_max, _ = loo_lambda(g, TH, wn, P)
    x = ridge_fit(g, TH, wn, P, lam)
    xt, xb, gap = implied_gap(x, pi, groups, top)
    nrep = N_RIDGE_REP if ridge else len(perms)
    pg, bg = [], []
    for pidx in perms[:nrep]:
        THp = TH[pidx]
        lp = loo_lambda(g, THp, wn, P)[0] if ridge else lam
        pg.append(implied_gap(ridge_fit(g, THp, wn, P, lp), pi, groups, top)[2])
    for bidx in boots[:nrep]:
        wb = w[bidx] / w[bidx].sum()
        lb = loo_lambda(g[bidx], TH[bidx], wb, P)[0] if ridge else lam
        bg.append(implied_gap(ridge_fit(g[bidx], TH[bidx], wb, P, lb), pi, groups, top)[2])
    pg, bg = np.array(pg), np.array(bg)
    cond = float(np.linalg.cond(TH.T @ (wn[:, None] * TH)))
    return dict(n=len(g), lam=lam, lam_at_grid_max=at_max, x=x, pi=pi, x_top20=xt, x_b80=xb, gap=gap,
                ci_boot_lo=float(np.percentile(bg, 2.5)), ci_boot_hi=float(np.percentile(bg, 97.5)),
                p_placebo=(1 + np.sum(np.abs(pg) >= abs(gap) - 1e-12)) / (len(pg) + 1), perm_sd=float(np.std(pg)),
                cond=cond, agg_growth=wmean(g, w), n_rep=nrep)


def zandi_gap(T):
    """Cumulative top20 - bottom80 gap over T years under Zandi's split (top +4%/yr, bottom 80% 0%/yr)."""
    return (1 + ZANDI_TOP) ** T - (1 + ZANDI_B80) ** T


def annualize_gap(x_b80, gap, T):
    """Per-year gap: (1 + x_b80 + gap)^(1/T) - (1 + x_b80)^(1/T). NaN when a bound implies the top group's
    spending fell by more than 100% (no meaningful annual rate)."""
    if not (np.isfinite(gap) and 1 + x_b80 + gap > 0 and 1 + x_b80 > 0):
        return np.nan
    return (1 + x_b80 + gap) ** (1 / T) - (1 + x_b80) ** (1 / T)


def make_perms(n, k=N_PERM, seed=0):
    r = np.random.default_rng(SEED + 7919 * n + seed)
    return np.array([r.permutation(n) for _ in range(k)])


def make_boots(n, k=N_BOOT, seed=0):
    r = np.random.default_rng(SEED + 104729 * n + seed)
    return np.array([r.integers(0, n, n) for _ in range(k)])

# %% 5. Samples (robustness drops) and the spec driver
# ---------------------------------------------------------------------------------------------------------
# 5. Samples (robustness drops) and the spec driver
# ---------------------------------------------------------------------------------------------------------
# A (16 major lines): health goods (in lines 7 and 12), net health insurance and FISIM (in line 20), imputed
# owners' rent and utilities (in line 15) cannot be split out at this level; whole lines are dropped instead.
A_DROPS = {"all": [], "drop_health": [16], "drop_imputed": [15, 20, 22], "drop_energy": [11], "drop_mv": [4]}
A_DROPS["drop_all4"] = sorted(set(sum(A_DROPS.values(), [])))


def b_drops(cats):
    d = {"all": [],
         "drop_health": [c for c in cats if in_subtree(c, [172, 121, 66, 275])],
         "drop_imputed": [c for c in cats if in_subtree(c, [160, 163, 254, 342])],
         "drop_energy": [c for c in cats if in_subtree(c, [113, 169])],
         "drop_mv": [c for c in cats if in_subtree(c, [5, 12])]}
    d["drop_all4"] = sorted(set(sum(d.values(), [])))
    return d


def theta_B(year):
    t = B_THETA[year].set_index("category")[[f"theta_{d}" for d in DEC]]
    return t.rename(columns=lambda s: s[6:])


MULTI_SPECS = {"4grp_ridge": ("4grp", None), "5grp_ridge": ("5grp", None), "4grp_ols": ("4grp", 0.0),
               "5grp_ols": ("5grp", 0.0)}


def run_specs(gf, theta_dec, drops, T, meta, specs=("2grp", "4grp_ridge", "5grp_ridge", "4grp_ols", "5grp_ols"),
              measures=("nominal", "real"), total_pce=None):
    """Every spec x sample x measure for one window/source. gf: growth frame (S0, g_nom, g_real by line)."""
    rows, cats_out = [], {}
    gz = zandi_gap(T)
    for sample, dropped in drops.items():
        keep = [c for c in theta_dec.index if c not in dropped and c in gf.index]
        w = gf.loc[keep, "S0"].to_numpy(float)
        thd = theta_dec.loc[keep]
        perms = make_perms(len(keep))
        boots = make_boots(len(keep))
        for measure in measures:
            g = gf.loc[keep, "g_nom" if measure == "nominal" else "g_real"].to_numpy(float)
            base = dict(meta, sample=sample, measure=measure, n_cats=len(keep), T_years=T,
                        coverage_of_pce=(w.sum() / total_pce) if total_pce else np.nan,
                        zandi_gap_cum=gz, zandi_gap_pa=ZANDI_TOP - ZANDI_B80)
            for spec in specs:
                if spec == "2grp":
                    th = thd[GROUPS["top20"]].sum(axis=1).to_numpy(float)
                    f = fit_2grp(g, th, w, gz, perms)
                    r = dict(base, spec=spec, x_b80=f["x_b80"], x_top20=f["x_top20"], gap=f["gap"],
                             ci_lo=f["ci_perm_lo"], ci_hi=f["ci_perm_hi"], ci_method="permutation test inversion",
                             ci_t_lo=f["ci_t_lo"], ci_t_hi=f["ci_t_hi"], se=f["se"], se_hc3=f["se_hc3"],
                             p_placebo=f["p_placebo"], p_zandi=f["p_zandi"], perm_sd=f["perm_sd"],
                             agg_growth=f["agg_growth"], theta_top20_bar=f["theta_bar"], kappa=f["kappa"],
                             basket_gap=f["basket_gap"], wrmse_fit=f["wrmse_fit"], wrmse_zandi=f["wrmse_zandi"],
                             wrmse_flat=f["wrmse_flat"], r2_fit_vs_flat=f["r2_fit_vs_flat"],
                             r2_zandi_vs_flat=f["r2_zandi_vs_flat"], mde80=f["mde80"],
                             ci_perm_at_edge=f["ci_perm_at_edge"])
                    if sample == "all":
                        cats_out[measure] = pd.DataFrame(dict(
                            category=keep, S0=w, share=w / w.sum(), g=g, theta_top20=th,
                            pred_fit=f["x_b80"] + f["gap"] * th,
                            pred_zandi=f["agg_growth"] + (th - f["theta_bar"]) * gz,
                            pred_flat=f["agg_growth"]))
                else:
                    gs, lam = MULTI_SPECS[spec]
                    groups = SPEC_GROUPS[gs]
                    TH = np.column_stack([thd[GROUPS[k]].sum(axis=1).to_numpy(float) for k in groups])
                    f = fit_groups(g, TH, w, groups, SPEC_TOP[gs], perms, boots, lam=lam)
                    pred = TH @ f["x"]
                    G = f["agg_growth"]
                    ssr_fit = np.sum(w * (g - pred) ** 2) / w.sum()
                    ssr_flat = np.sum(w * (g - G) ** 2) / w.sum()
                    r = dict(base, spec=spec, x_b80=f["x_b80"], x_top20=f["x_top20"], gap=f["gap"],
                             ci_lo=f["ci_boot_lo"], ci_hi=f["ci_boot_hi"], ci_method=("pairs bootstrap, lambda re-selected per replicate" if spec.endswith("ridge") else "pairs bootstrap"),
                             p_placebo=f["p_placebo"], perm_sd=f["perm_sd"], agg_growth=G,
                             wrmse_fit=np.sqrt(ssr_fit), wrmse_flat=np.sqrt(ssr_flat),
                             r2_fit_vs_flat=1 - ssr_fit / ssr_flat, lam=f["lam"], lam_at_grid_max=f["lam_at_grid_max"],
                             cond=f["cond"], x_groups=";".join(f"{k}={v:+.4f}" for k, v in zip(groups, f["x"])))
                r["gap_pa"] = annualize_gap(r["x_b80"], r["gap"], T)
                r["gap_pa_ci_lo"] = annualize_gap(r["x_b80"], r["ci_lo"], T) if np.isfinite(r["ci_lo"]) else np.nan
                r["gap_pa_ci_hi"] = annualize_gap(r["x_b80"], r["ci_hi"], T) if np.isfinite(r["ci_hi"]) else np.nan
                r["x_top20_pa"] = (1 + r["x_top20"]) ** (1 / T) - 1
                r["x_b80_pa"] = (1 + r["x_b80"]) ** (1 / T) - 1
                r["zandi_inside_ci"] = bool(r["ci_lo"] <= gz <= r["ci_hi"])
                r["zero_inside_ci"] = bool(r["ci_lo"] <= 0 <= r["ci_hi"])
                rows.append(r)
    return rows, cats_out


# %% 6. Backtest on source A (where the dPCE gives group totals)
# ---------------------------------------------------------------------------------------------------------
# 6. Backtest on source A (where the dPCE gives group totals)
# ---------------------------------------------------------------------------------------------------------
# The dPCE builds each year's group spending as that year's category totals x CE-based decile shares. So the
# backtest is a consistency test of the inverse estimator against within-category share drift (plus, in the
# 'nipa' variant, NIPA revisions since the dPCE vintage), not an independent measurement of group spending.
BACKTEST_WINDOWS = [(2003, 2007), (2007, 2009), (2009, 2013), (2016, 2019), (2019, 2023), (2021, 2023)]


def dpce_growth_frame(y0, y1):
    s0 = DP_PCE.loc[y0, A_CATS].astype(float)
    s1 = DP_PCE.loc[y1, A_CATS].astype(float)
    return pd.DataFrame(dict(S0=s0, S1=s1, g_nom=s1 / s0 - 1, g_real=np.nan))


bt_rows = []
for (y0, y1) in tqdm(BACKTEST_WINDOWS, desc="backtest windows (A)"):
    thd = theta_A(y0)
    T = y1 - y0
    variants = [("nominal", "dpce_totals", dpce_growth_frame(y0, y1)),
                ("nominal", "nipa_current", growth_frame("A", A_CATS, str(y0), str(y1), "A")),
                ("real", "nipa_current", growth_frame("A", A_CATS, str(y0), str(y1), "A"))]
    for measure, gsrc, gf in variants:
        meta = dict(window=f"{y0}->{y1}", t0=str(y0), t1=str(y1), source="A_dPCE", theta_base_year=y0,
                    growth_source=gsrc)
        rows, _ = run_specs(gf, thd, {"all": []}, T, meta, specs=("2grp", "4grp_ridge", "5grp_ridge"),
                            measures=(measure,))
        act = dpce_group_growth(y0, y1, ALL_GROUPS, real=(measure == "real"))
        for r in rows:
            r["gap_actual"] = act["top20"] - act["b80"]
            r["x_top20_actual"], r["x_b80_actual"] = act["top20"], act["b80"]
            r["gap_error"] = r["gap"] - r["gap_actual"]
            r["gap_actual_pa"] = annualize_gap(act["b80"], r["gap_actual"], T)
            r["gap_error_pa"] = r["gap_pa"] - r["gap_actual_pa"]
            r["actual_inside_ci"] = bool(r["ci_lo"] <= r["gap_actual"] <= r["ci_hi"])
            if r["spec"] == "2grp":
                r["basket_error"] = r["basket_gap"] - r["gap_actual"]
            if r["spec"] == "5grp_ridge":
                xs = dict(kv.split("=") for kv in r["x_groups"].split(";"))
                for q in SPEC_GROUPS["5grp"]:
                    r[f"x_{q}_est"] = float(xs[q])
                    r[f"x_{q}_actual"] = act[q]
            r["dpce_total_growth"] = (DP_PCE.at[y1, 1] / DP_PCE.at[y0, 1] - 1) if measure == "nominal" else np.nan
            bt_rows.append(r)
for r in bt_rows:
    r["actual_source"] = "dPCE T1 decile shares x totals" + (" / T3 decile prices" if r["measure"] == "real" else "")


def ce_inscope_fraction(year):
    """Share of each B item's all-CU mean that sits in UCCs with a PCE target (each UCC counted once)."""
    lk = B_LINKS[year]
    m = lk[lk.pce_line.notna()].drop_duplicates(["item_key", "ucc"])
    num = m.groupby("item_key").ucc_mean_all.apply(lambda s: s.clip(lower=0).sum())
    it = B_ITEMS[year]
    return (num / it.mean_all).clip(upper=1.0).reindex(it.index).fillna(0.0)


def ce_group_growth(y0, y1, groups, scope):
    """CE Table 1110 group spending growth (nominal): 'total' = average annual expenditures x CU counts;
    'pce_scope' = B items x their in-scope fraction (owner rental equivalence excluded)."""
    out = {}
    tot = {}
    for y in (y0, y1):
        N, _ = ce_counts(y)
        if scope == "total":
            t, _ = ce_item_table(y)
            m = t.loc["Average annual expenditures", DEC].astype(float)
        else:
            it = B_ITEMS[y]
            f = ce_inscope_fraction(y)
            keep = [k for k in it.index if not k.startswith("Addenda")]
            m = pd.Series({d: float((it.loc[keep, f"mean_{d}"] * f[keep]).sum()) for d in DEC})
        tot[y] = N * m
    for gname in groups:
        out[gname] = tot[y1][GROUPS[gname]].sum() / tot[y0][GROUPS[gname]].sum() - 1
    return out


B_BT_WINDOWS = [(2014, 2016), (2016, 2019), (2019, 2021), (2021, 2023), (2019, 2023), (2023, 2025), (2022, 2025)]
for (y0, y1) in tqdm(B_BT_WINDOWS, desc="B vs CE group totals"):
    thd = theta_B(y0)
    gf = growth_frame("U", list(thd.index), str(y0), str(y1), "A")
    for measure in ("nominal", "real"):
        meta = dict(window=f"{y0}->{y1}", t0=str(y0), t1=str(y1), source="B_CE", theta_base_year=y0,
                    growth_source="nipa_current")
        rows, _ = run_specs(gf, thd, {"all": []}, y1 - y0, meta, specs=("2grp",), measures=(measure,))
        for scope in ("total", "pce_scope"):
            act = ce_group_growth(y0, y1, ["top20", "b80"], scope)
            for r in rows:
                r = dict(r)
                r["gap_actual"] = act["top20"] - act["b80"]
                r["x_top20_actual"], r["x_b80_actual"] = act["top20"], act["b80"]
                r["gap_error"] = r["gap"] - r["gap_actual"]
                r["gap_actual_pa"] = annualize_gap(act["b80"], r["gap_actual"], y1 - y0)
                r["gap_error_pa"] = r["gap_pa"] - r["gap_actual_pa"]
                r["actual_inside_ci"] = bool(r["ci_lo"] <= r["gap_actual"] <= r["ci_hi"])
                r["actual_source"] = (f"CE Table 1110 nominal group spending ({scope}); income-ranked survey, "
                                      f"not a national-accounts truth")
                bt_rows.append(r)
BACKTEST = pd.DataFrame(bt_rows)
BACKTEST.to_csv(OUT / "fingerprint_backtest.csv", index=False, float_format="%.10g")

# %% 7. The read
# ---------------------------------------------------------------------------------------------------------
# 7. The read: 2023 -> 2025 (annual), 2023-09 -> 2026-09 and 2022-09 -> 2026-09 (monthly)
# ---------------------------------------------------------------------------------------------------------
READ_WINDOWS = [("2023->2025", "A", "2023", "2025", 2.0),
                ("2023-09->2026-09", "M", "2023-09", "2026-09", 3.0),
                ("2022-09->2026-09", "M", "2022-09", "2026-09", 4.0)]
READ_THETA = {"A_dPCE": {"2023->2025": [2023], "2023-09->2026-09": [2023], "2022-09->2026-09": [2023, 2022]},
              "B_CE": {"2023->2025": [2024, 2023, 2025], "2023-09->2026-09": [2024, 2023, 2025],
                       "2022-09->2026-09": [2024, 2022]}}
MAIN_THETA = {"A_dPCE": 2023, "B_CE": 2024}

rd_rows, rd_cats = [], []
jobs = [(w, src, yb) for w in READ_WINDOWS for src in READ_THETA for yb in READ_THETA[src][w[0]]]
for (win, freq, t0, t1, T), src, yb in tqdm(jobs, desc="read: window x source x theta year"):
    if src == "A_dPCE":
        thd = theta_A(yb)
        gf = growth_frame("A", A_CATS, t0, t1, freq)
        drops = A_DROPS
    else:
        thd = theta_B(yb)
        gf = growth_frame("U", list(thd.index), t0, t1, freq)
        drops = b_drops(list(thd.index))
    total = float(W[("2.4.5U", freq)].at[t0, 1])
    meta = dict(window=win, freq=freq, t0=t0, t1=t1, source=src, theta_base_year=yb,
                theta_role="main" if yb == MAIN_THETA[src] else "sensitivity")
    rows, cats = run_specs(gf, thd, drops, T, meta, total_pce=total)
    rd_rows += rows
    for measure, cf in cats.items():
        cf = cf.assign(window=win, source=src, theta_base_year=yb, measure=measure,
                       label=[A_SHORT.get(c, "") if src == "A_dPCE" else ULABEL[c] for c in cf.category])
        rd_cats.append(cf)
READ = pd.DataFrame(rd_rows)
READ_CATS = pd.concat(rd_cats, ignore_index=True)

# eta variant (Working-model elasticities eta = 1 + beta / w): only if the USDA TB-1929 parameters are tidied
ETA_FILE = TIDY / "usda_tb1929_params.csv"
ETA_STATUS = ("skipped: consumption/data/tidy/usda_tb1929_params.csv does not exist" if not ETA_FILE.exists()
              else "file present: see NOTES (variant not implemented in this run)")
READ["eta_variant"] = ETA_STATUS
READ.to_csv(OUT / "fingerprint_read.csv", index=False, float_format="%.10g")
READ_CATS.to_csv(OUT / "fingerprint_read_categories.csv", index=False, float_format="%.10g")

# influence: which categories carry the two-group slope (main theta, all categories)
inf_rows = []
for (win, freq, t0, t1, T) in READ_WINDOWS:
    for src in ("A_dPCE", "B_CE"):
        for measure in ("nominal", "real"):
            cf = READ_CATS[(READ_CATS.window == win) & (READ_CATS.source == src)
                           & (READ_CATS.theta_base_year == MAIN_THETA[src]) & (READ_CATS.measure == measure)]
            g, th, w = cf.g.to_numpy(float), cf.theta_top20.to_numpy(float), cf.S0.to_numpy(float)
            a, b = wls_line(g, th, w)
            wn = w / w.sum()
            tb, gb = np.sum(wn * th), np.sum(wn * g)
            sxx = np.sum(wn * (th - tb) ** 2)
            contrib = wn * (th - tb) * (g - gb) / sxx
            for i in range(len(g)):
                keep = np.arange(len(g)) != i
                bi = wls_line(g[keep], th[keep], w[keep])[1]
                inf_rows.append(dict(window=win, source=src, measure=measure, category=int(cf.category.iloc[i]),
                                     label=cf.label.iloc[i], share=wn[i], theta_top20=th[i], g=g[i],
                                     contrib_to_slope=contrib[i], gap_all=b, gap_without=bi, delta=bi - b))
INFL = pd.DataFrame(inf_rows)
INFL.to_csv(OUT / "fingerprint_influence.csv", index=False, float_format="%.10g")

# %% 8. Power
# ---------------------------------------------------------------------------------------------------------
# 8. Power: the estimator's noise in windows where the answer is known (A) or in quiet history (B)
# ---------------------------------------------------------------------------------------------------------
pw_rows = []
for T in tqdm((2, 3, 4), desc="power: A rolling annual windows"):
    for y0 in range(2000, 2024 - T):
        y1 = y0 + T
        th = theta_A(y0)[GROUPS["top20"]].sum(axis=1)
        gfn = growth_frame("A", A_CATS, str(y0), str(y1), "A")
        for measure, gsrc, gf in (("nominal", "dpce_totals", dpce_growth_frame(y0, y1)),
                                  ("nominal", "nipa_current", gfn), ("real", "nipa_current", gfn)):
            g = gf["g_nom" if measure == "nominal" else "g_real"].to_numpy(float)
            a, b = wls_line(g, th.to_numpy(float), gf.S0.to_numpy(float))
            act = dpce_group_growth(y0, y1, ["top20", "b80"], real=(measure == "real"))
            pw_rows.append(dict(kind="A_rolling_annual", source="A_dPCE", T_years=T, t0=str(y0), t1=str(y1),
                                measure=measure, growth_source=gsrc, gap=b,
                                gap_actual=act["top20"] - act["b80"], gap_error=b - (act["top20"] - act["b80"])))
for T in tqdm((2, 3, 4), desc="power: B rolling annual windows"):
    for y0 in range(2014, 2026 - T):
        y1 = y0 + T
        thd = theta_B(y0)
        th = thd[GROUPS["top20"]].sum(axis=1)
        gf = growth_frame("U", list(thd.index), str(y0), str(y1), "A")
        act = ce_group_growth(y0, y1, ["top20", "b80"], "total")
        for measure in ("nominal", "real"):
            g = gf["g_nom" if measure == "nominal" else "g_real"].to_numpy(float)
            a, b = wls_line(g, th.to_numpy(float), gf.S0.to_numpy(float))
            pw_rows.append(dict(kind="B_rolling_annual", source="B_CE", T_years=T, t0=str(y0), t1=str(y1),
                                measure=measure, growth_source="nipa_current", gap=b,
                                gap_actual_ce_nominal=act["top20"] - act["b80"],
                                gap_actual=act["top20"] - act["b80"], gap_error=b - (act["top20"] - act["b80"]),
                                error_basis="CE Table 1110 nominal group totals (income-ranked survey; for the "
                                            "real estimate the nominal CE gap stands in, a common deflator barely "
                                            "moves a gap)"))


def month_add(m, k):
    p = pd.Period(m, freq="M") + k
    return str(p)


months_all = list(W[("2.8.5", "M")].index)
for src, start in (("A_dPCE", "2007-01"), ("B_CE", "2014-01")):
    for L in (36, 48):
        for m0 in tqdm([m for m in months_all if m >= start and month_add(m, L) <= months_all[-1]],
                       desc=f"power: {src} rolling {L}-month windows"):
            m1 = month_add(m0, L)
            yb = int(m0[:4])
            if src == "A_dPCE":
                th = theta_A(min(yb, 2023))[GROUPS["top20"]].sum(axis=1)
                gf = growth_frame("A", A_CATS, m0, m1, "M")
            else:
                thd = theta_B(yb)
                th = thd[GROUPS["top20"]].sum(axis=1)
                gf = growth_frame("U", list(thd.index), m0, m1, "M")
            for measure in ("nominal", "real"):
                g = gf["g_nom" if measure == "nominal" else "g_real"].to_numpy(float)
                a, b = wls_line(g, th.to_numpy(float), gf.S0.to_numpy(float))
                pw_rows.append(dict(kind=f"{src[0]}_rolling_{L}m", source=src, T_years=L / 12, t0=m0, t1=m1,
                                    measure=measure, growth_source="nipa_current", gap=b))
POWER = pd.DataFrame(pw_rows)

# Calm-period norm: windows that start after the 2008-09 recession (A: 2010 on; B: its first year, 2014) and end
# before 2020. In those years no K of Zandi's size shows in the dPCE or the CE, so the mean estimate there is the
# estimator's normal reading (Engel effects, secular trends, quality adjustment) and the spread is its quiet-time
# noise. The read's 'excess over the calm norm' compares like with like (same source, length and measure).
CALM_START = {"A_dPCE": "2010", "B_CE": "2014"}


def is_calm(src, t0, t1):
    return str(t0)[:4] >= CALM_START[src] and str(t1) <= "2019-12"


LATEST = {36: "2023-09", 48: "2022-09", 2: "2023"}
z975, z80 = stats.norm.ppf(0.975), stats.norm.ppf(0.8)
summ = []
for (kind, T, measure, gsrc), x in POWER.groupby(["kind", "T_years", "measure", "growth_source"]):
    src = x.source.iloc[0]
    r = dict(kind="summary:" + kind, source=src, T_years=T, measure=measure, growth_source=gsrc, n_windows=len(x),
             gap_mean=x.gap.mean(), gap_sd=x.gap.std(), zandi_gap_cum=zandi_gap(T))
    if "gap_error" in x and x.gap_error.notna().any():
        sd = x.gap_error.std()
        r.update(err_mean=x.gap_error.mean(), err_sd=sd, err_rmse=float(np.sqrt(np.mean(x.gap_error ** 2))),
                 actual_gap_mean=x.gap_actual.mean(), actual_gap_sd=x.gap_actual.std(),
                 mde80_from_err_sd=(z975 + z80) * sd,
                 power_vs_zandi_err=float(stats.norm.cdf(zandi_gap(T) / sd - z975)))
    calm = x[[is_calm(src, a, b) for a, b in zip(x.t0, x.t1)]]
    if len(calm) >= 3:
        cm, cs = calm.gap.mean(), calm.gap.std()
        r.update(calm_n=len(calm), calm_mean=cm, calm_sd=cs, calm_min=calm.gap.min(), calm_max=calm.gap.max(),
                 mde80_calm=(z975 + z80) * cs, power_vs_zandi_calm=float(stats.norm.cdf(zandi_gap(T) / cs - z975)))
        lk = LATEST.get(int(round(T * 12))) if kind.endswith("m") else ("2023" if T == 2 else None)
        last = x[x.t0 == lk] if lk else x.iloc[0:0]
        if len(last):
            v = float(last.gap.iloc[0])
            r.update(latest_t0=lk, latest_gap=v, latest_excess_over_calm=v - cm, latest_z_vs_calm=(v - cm) / cs,
                     latest_share_calm_above=float((calm.gap >= v).mean()),
                     zandi_z_vs_calm=(v - cm - zandi_gap(T)) / cs)
    if kind.startswith("B_rolling_annual"):
        r.update(ce_actual_gap_mean=x.gap_actual_ce_nominal.mean(), ce_actual_gap_sd=x.gap_actual_ce_nominal.std())
    summ.append(r)
POWER_SUMMARY = pd.DataFrame(summ)
pd.concat([POWER, POWER_SUMMARY], ignore_index=True).to_csv(OUT / "fingerprint_power.csv", index=False,
                                                            float_format="%.10g")

# Two benchmarks attached to the read (two-group rows):
# (1) historically calibrated band: the estimator's error where group totals are known (A: dPCE; B: CE survey
#     totals), annual windows of the same length; rolling windows overlap, so it is a scale, not an exact interval;
# (2) calm-period norm: mean and spread of the estimate in 2010/2014-2019 windows of the same length (monthly 36 and
#     48 months for the monthly read windows, annual 2-year windows for 2023->2025); excess = estimate - norm, and
#     Zandi's split adds his gap on top of the norm.
HIST = POWER_SUMMARY[POWER_SUMMARY.kind.isin(["summary:A_rolling_annual", "summary:B_rolling_annual"])
                     & POWER_SUMMARY.growth_source.eq("nipa_current")]
hist_map = {(r.source, float(r.T_years), r.measure): (r.err_mean, r.err_sd, r.n_windows) for r in HIST.itertuples()}
CALM = POWER_SUMMARY[POWER_SUMMARY.growth_source.eq("nipa_current") & POWER_SUMMARY.calm_n.notna()]
calm_map = {}
for r in CALM.itertuples():
    k = r.kind.replace("summary:", "")
    win = {"36m": "2023-09->2026-09", "48m": "2022-09->2026-09"}.get(k.split("_")[-1], "2023->2025"
                                                                     if k.endswith("annual") and r.T_years == 2 else None)
    if win:
        calm_map[(r.source, win, r.measure)] = (r.calm_mean, r.calm_sd, r.calm_n)


def bench_cols(r):
    out = dict(hist_err_mean=np.nan, hist_err_sd=np.nan, hist_n_windows=np.nan, gap_hist_lo=np.nan,
               gap_hist_hi=np.nan, calm_norm_mean=np.nan, calm_norm_sd=np.nan, calm_n_windows=np.nan,
               excess_over_calm=np.nan, excess_z=np.nan, zandi_z_vs_calm=np.nan)
    if r["spec"] != "2grp":
        return pd.Series(out)
    k = (r["source"], float(r["T_years"]), r["measure"])
    if k in hist_map:
        m, sd, n = hist_map[k]
        out.update(hist_err_mean=m, hist_err_sd=sd, hist_n_windows=n, gap_hist_lo=r["gap"] - z975 * sd,
                   gap_hist_hi=r["gap"] + z975 * sd)
    k = (r["source"], r["window"], r["measure"])
    if k in calm_map:
        cm, cs, cn = calm_map[k]
        ex = r["gap"] - cm
        out.update(calm_norm_mean=cm, calm_norm_sd=cs, calm_n_windows=cn, excess_over_calm=ex, excess_z=ex / cs,
                   zandi_z_vs_calm=(ex - r["zandi_gap_cum"]) / cs)
    return pd.Series(out)


READ = pd.concat([READ, READ.apply(bench_cols, axis=1)], axis=1)
READ.to_csv(OUT / "fingerprint_read.csv", index=False, float_format="%.10g")

# %% 9. Top-tilt index (descriptive)
# ---------------------------------------------------------------------------------------------------------
# 9. Top-tilt index (descriptive): real growth of the top-20 basket minus the bottom-80 basket
# ---------------------------------------------------------------------------------------------------------
# Basket weights: each group's budget shares in the base year, omega_qg = theta_qg S_g / sum_g theta_qg S_g, fixed
# within a link and chained by base year. tilt = sum_g (omega_top,g - omega_b80,g) q_g with q_g real growth.
# Identity (same weights): tilt = kappa x (two-group WLS slope); implied_gap = tilt / kappa.
NBER = [("2001-03", "2001-11"), ("2007-12", "2009-06"), ("2020-02", "2020-04")]   # NBER peak -> trough months


def in_recession(m):
    return any(a < m <= b for a, b in NBER)


def tilt_from(th, S, q):
    th, S, q = np.asarray(th, float), np.asarray(S, float), np.asarray(q, float)
    om_t = th * S / np.sum(th * S)
    om_b = (1 - th) * S / np.sum((1 - th) * S)
    w = S / S.sum()
    k = kappa(th, w)
    top, bot = float(np.sum(om_t * q)), float(np.sum(om_b * q))
    return top, bot, top - bot, k


tilt_a = []
lev_t, lev_b = 100.0, 100.0
for y in range(2001, 2026):
    yb = min(y - 1, 2023)
    th = theta_A(yb)[GROUPS["top20"]].sum(axis=1)
    gf = growth_frame("A", A_CATS, str(y - 1), str(y), "A")
    top, bot, tl, k = tilt_from(th, gf.S0, gf.g_real)
    lev_t *= 1 + top
    lev_b *= 1 + bot
    tilt_a.append(dict(year=y, source="A_dPCE", theta_base_year=yb, weights_year=y - 1, top20_basket=top,
                       b80_basket=bot, tilt=tl, kappa=k, implied_gap=tl / k, zandi_tilt=k * (ZANDI_TOP - ZANDI_B80),
                       top20_index=lev_t, b80_index=lev_b, tilt_index=100 * lev_t / lev_b,
                       nber_recession_year=any(a[:4] <= str(y) <= b[:4] for a, b in NBER), covid_2020=(y == 2020)))
TILT_A = pd.DataFrame(tilt_a)
TILT_A.to_csv(OUT / "fingerprint_top_tilt_annual.csv", index=False, float_format="%.10g")

tilt_m = []
for src, first in (("A_dPCE", "2007-01"), ("B_CE", "2015-01")):
    for m in tqdm([m for m in months_all if m >= first], desc=f"top tilt monthly {src}"):
        m0 = month_add(m, -12)
        yw = int(m0[:4])
        if src == "A_dPCE":
            yb = min(yw, 2023)
            th = theta_A(yb)[GROUPS["top20"]].sum(axis=1)
            gf = growth_frame("A", A_CATS, m0, m, "M")
            S = W[("2.3.5", "A")].loc[str(yw), A_CATS]
        else:
            yb = yw
            thd = theta_B(yb)
            th = thd[GROUPS["top20"]].sum(axis=1)
            gf = growth_frame("U", list(thd.index), m0, m, "M")
            S = W[("2.4.5U", "A")].loc[str(yw), list(thd.index)]
        top, bot, tl, k = tilt_from(th.loc[gf.index], S.loc[gf.index], gf.g_real)
        tilt_m.append(dict(date=m, source=src, theta_base_year=yb, weights_year=yw, top20_basket_12m=top,
                           b80_basket_12m=bot, tilt_12m=tl, kappa=k, implied_gap_12m=tl / k,
                           zandi_tilt_12m=k * (ZANDI_TOP - ZANDI_B80),
                           real_source=",".join(sorted(set(gf.real_source))),
                           nber_recession=in_recession(m), covid_2020=m.startswith("2020")))
TILT_M = pd.DataFrame(tilt_m)
TILT_M.to_csv(OUT / "top_tilt_monthly.csv", index=False, float_format="%.10g")

# %% 10. Charts
# ---------------------------------------------------------------------------------------------------------
# 10. Charts (dataviz skill: reference palette, light surface, hairline grid, 2px-equivalent lines, legend for
#     two or more series plus selective direct labels, text in ink tokens, no dual axes). PNG at 200 dpi.
# ---------------------------------------------------------------------------------------------------------
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
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


def pct(x, _=None):
    return f"{100 * x:+.0f}%" if x != 0 else "0%"


# --- scatter: category real growth 2023-09 -> 2026-09 against theta_top20, A and B --------------------------
SC_WIN = "2023-09->2026-09"
SHORT_B = {154: "Tenant rent", 141: "Tobacco", 177: "Home health care", 291: "Higher education",
           123: "Prescription drugs", 71: "Telephone equipment", 6: "New autos", 9: "New light trucks",
           115: "Gasoline", 334: "Foreign travel", 200: "Ground transportation", 210: "Clubs, parks, theaters"}
from matplotlib.ticker import MultipleLocator
fig, axes = plt.subplots(1, 2, figsize=(12, 5.6), gridspec_kw=dict(wspace=0.18))
for ax, src in zip(axes, ("A_dPCE", "B_CE")):
    style_axes(ax)
    cf = READ_CATS[(READ_CATS.window == SC_WIN) & (READ_CATS.source == src)
                   & (READ_CATS.theta_base_year == MAIN_THETA[src]) & (READ_CATS.measure == "real")].copy()
    rr = READ[(READ.window == SC_WIN) & (READ.source == src) & (READ.theta_base_year == MAIN_THETA[src])
              & (READ.measure == "real") & (READ["sample"] == "all") & (READ.spec == "2grp")].iloc[0]
    lo, hi = np.percentile(cf.g, [1, 99]) if src == "B_CE" else (cf.g.min(), cf.g.max())
    pad = 0.08 * (hi - lo)
    ylo, yhi = lo - pad, hi + pad
    inside = cf[(cf.g >= ylo) & (cf.g <= yhi)]
    outside = cf[(cf.g < ylo) | (cf.g > yhi)]
    size = 2400 * inside.share / cf.share.max() * (0.35 if src == "B_CE" else 0.42)
    ax.scatter(inside.theta_top20, inside.g, s=size + 6, color=BLUE, alpha=0.45, edgecolor=SURF, linewidth=1.2,
               zorder=3, label="category (area = 2023-09 spending)")
    for _, r in outside.iterrows():
        yy = yhi if r.g > yhi else ylo
        ax.scatter([r.theta_top20], [yy], marker="^" if r.g > yhi else "v", s=36, color=BLUE, alpha=0.8,
                   edgecolor=SURF, linewidth=1.0, zorder=3)
        right = r.theta_top20 > 0.5
        nm = SHORT_B.get(int(r.category), r.label[:22]) if src == "B_CE" else r.label
        ax.annotate(f"{nm} ({100 * r.g:+.0f}%, off scale)", (r.theta_top20, yy),
                    xytext=(-6 if right else 6, -10 if r.g > yhi else 4), textcoords="offset points", fontsize=7,
                    color=INK2, ha="right" if right else "left")
    xs = np.linspace(cf.theta_top20.min() - 0.01, cf.theta_top20.max() + 0.01, 50)
    tb = rr.theta_top20_bar
    lines = [(rr.x_b80 + rr.gap * xs, BLUE, f"fitted: gap {100 * rr.gap:+.1f} pts"),
             (rr.agg_growth + (xs - tb) * rr.zandi_gap_cum, ORANGE, f"Zandi split: {100 * rr.zandi_gap_cum:+.1f} pts"),
             (np.full_like(xs, rr.agg_growth), MUTED, "flat: 0 pts")]
    for y, col, lab in lines:
        ax.plot(xs, y, color=col, lw=1.6, solid_capstyle="round", zorder=4, label=lab)
        if src == "A_dPCE":                   # in B the three lines converge at the right edge: legend only
            ax.annotate(lab.split(":")[0], (xs[-1], y[-1]), xytext=(4, 0), textcoords="offset points",
                        fontsize=7.5, color=INK2, va="center")
    # selective labels: the four categories that move the slope most
    if src == "B_CE":
        inf = INFL[(INFL.window == SC_WIN) & (INFL.source == src) & (INFL.measure == "real")]
        lab_cats = list(inf.reindex(inf.contrib_to_slope.abs().sort_values(ascending=False).index).category[:5])
    else:
        lab_cats = list(cf.reindex((cf.g - cf.pred_fit).abs().sort_values(ascending=False).index).category[:6])
    for _, r in inside[inside.category.isin(lab_cats)].iterrows():
        right = r.theta_top20 > (0.5 if src == "B_CE" else 0.6)
        below = src == "B_CE" and int(r.category) == 154       # tenant rent sits on the lines' left end
        nm = SHORT_B.get(int(r.category), r.label[:30]) if src == "B_CE" else r.label
        ax.annotate(nm, (r.theta_top20, r.g), xytext=(-6 if right else 6, -11 if below else 5),
                    textcoords="offset points", fontsize=7, color=INK2, ha="right" if right else "left")
    ax.set_ylim(ylo, yhi)
    ax.yaxis.set_major_locator(MultipleLocator(0.04 if src == "A_dPCE" else 0.10))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(pct))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{100 * v:.0f}%"))
    ax.set_xlabel(f"top 20% share of the category's spending (theta, base year {MAIN_THETA[src]})")
    ttl = ("A: 16 major product lines, BLS distributional PCE (spending-ranked deciles)" if src == "A_dPCE"
           else f"B: {len(cf)} PCE lines, CE income deciles mapped through UCCs")
    ax.text(0, 1.005, f"gap {100 * rr.gap:+.1f} pts (95% perm. CI {100 * rr.ci_lo:+.0f} to {100 * rr.ci_hi:+.0f}); "
            f"placebo p = {rr.p_placebo:.2f}; Zandi's split {100 * rr.zandi_gap_cum:+.1f} pts, p = {rr.p_zandi:.2f}",
            transform=ax.transAxes, fontsize=7.8, color=INK2, va="bottom")
    ax.set_title(ttl, loc="left", fontsize=9.5, pad=16)
axes[0].set_ylabel("real growth of category, 2023-09 to 2026-09")
h, l = axes[1].get_legend_handles_labels()
fig.legend(h[1:] + h[:1], ["fitted (WLS)", "Zandi split (top +4%/yr, bottom 80% 0)", "flat (all groups alike)",
                           "category (area = spending)"], loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.01))
fig.suptitle("Do the categories the top 20% buy outgrow the rest? Real category growth vs the top 20% market share",
             x=0.06, ha="left", fontsize=11, fontweight="bold", y=0.995)
fig.subplots_adjust(left=0.06, right=0.95, top=0.86, bottom=0.17)
fig.savefig(FIG / "fig_fingerprint_scatter.png", dpi=200)
plt.close(fig)

# --- backtest: estimated vs actual gap, annualized, A (nominal dPCE totals, real) and B vs CE (nominal) ----
fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.8), sharey=True, gridspec_kw=dict(wspace=0.10))
panels = [("A: nominal (dPCE category totals)", (BACKTEST.source == "A_dPCE") & (BACKTEST.growth_source == "dpce_totals")
           & (BACKTEST.measure == "nominal"), "actual dPCE gap"),
          ("A: real (NIPA quantities; dPCE / T3 prices)", (BACKTEST.source == "A_dPCE") & (BACKTEST.measure == "real"),
           "actual dPCE gap"),
          ("B: nominal, against CE survey group totals", (BACKTEST.source == "B_CE") & (BACKTEST.measure == "nominal")
           & BACKTEST.actual_source.str.contains("(total)", regex=False), "CE survey gap (total spending)")]
for ax, (ttl, mask, actlab) in zip(axes, panels):
    style_axes(ax)
    x = BACKTEST[mask & (BACKTEST.spec == "2grp")].reset_index(drop=True)
    pos = np.arange(len(x))
    ax.axhline(0, color=AXIS, lw=0.8, zorder=1)
    ax.axhline(ZANDI_TOP - ZANDI_B80, color=ORANGE, lw=1.4, zorder=2)
    ax.vlines(pos, x.gap_pa_ci_lo, x.gap_pa_ci_hi, color=BLUE, lw=1.6, alpha=0.55, zorder=3)
    ax.scatter(pos, x.gap_pa, s=42, color=BLUE, edgecolor=SURF, linewidth=1.4, zorder=4, label="estimate, 95% CI")
    ax.scatter(pos, x.gap_actual_pa, s=46, marker="D", color=INK, edgecolor=SURF, linewidth=1.4, zorder=5,
               label=actlab)
    ax.set_xticks(pos, [w.replace("->", "\n–") for w in x.window], rotation=0, fontsize=7.6)
    ax.set_xlim(-0.6, len(x) - 0.4)
    ax.set_title(ttl, loc="left", fontsize=9)
    ax.grid(axis="x", visible=False)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{100 * v:+.0f}" if v else "0"))
axes[0].set_ylabel("top 20% minus bottom 80% spending growth, points a year")
from matplotlib.lines import Line2D
fig.legend([Line2D([], [], color=BLUE, marker="o", lw=1.6, alpha=0.8, markeredgecolor=SURF, markersize=6),
            Line2D([], [], color=INK, marker="D", lw=0, markeredgecolor=SURF, markersize=6),
            Line2D([], [], color=ORANGE, lw=1.4)],
           ["estimate (two-group WLS) with 95% interval", "actual gap: dPCE group totals (A), CE survey totals (B)",
            "Zandi's split: +4 points a year"], loc="lower center", ncol=3, bbox_to_anchor=(0.5, 0.045))
lo_all = min(BACKTEST.gap_pa_ci_lo.min(), -0.3)
hi_all = max(BACKTEST.gap_pa_ci_hi.max(), 0.3)
axes[0].set_ylim(max(lo_all, -0.45), min(hi_all, 0.45))
fig.suptitle("Backtest: the inverse estimator against group totals where they are known (two groups, annualized)",
             x=0.06, ha="left", fontsize=11, fontweight="bold")
fig.text(0.07, 0.008, "Intervals clipped at \u00b145 points a year. A's 'actual' is built from the same category totals "
         "times CE-based shares, so it tests the estimator against within-category share drift, not an independent "
         "measurement.", fontsize=7.5, color=MUTED)
fig.subplots_adjust(left=0.07, right=0.98, top=0.86, bottom=0.25)
fig.savefig(FIG / "fig_fingerprint_backtest.png", dpi=200)
plt.close(fig)

# --- top tilt: 12-month tilt and implied gap, monthly -------------------------------------------------------
fig, axes = plt.subplots(2, 1, figsize=(12, 7.2), sharex=True, gridspec_kw=dict(hspace=0.16, height_ratios=[1, 1]))
tm = TILT_M.copy()
tm["dt"] = pd.PeriodIndex(tm.date, freq="M").to_timestamp()
for ax in axes:
    style_axes(ax)
    for a, b in NBER:
        if b >= "2007-01":
            ax.axvspan(pd.Period(a, "M").to_timestamp(), pd.Period(b, "M").to_timestamp(), color=GRID, alpha=0.9,
                       lw=0, zorder=0)
    ax.axvspan(pd.Timestamp("2020-01-01"), pd.Timestamp("2020-12-31"), color=GRID, alpha=0.45, lw=0, zorder=0)
    ax.axhline(0, color=AXIS, lw=0.8, zorder=1)
for src, col, lab in (("A_dPCE", BLUE, "A: 16 lines, dPCE theta"), ("B_CE", AQUA, "B: CE-mapped PCE lines")):
    x = tm[tm.source == src]
    axes[0].plot(x.dt, x.tilt_12m, color=col, lw=1.4, label=lab)
    axes[1].plot(x.dt, x.implied_gap_12m, color=col, lw=1.4, label=lab)
za = tm[tm.source == "A_dPCE"]
axes[0].plot(za.dt, za.zandi_tilt_12m, color=ORANGE, lw=1.2, label="tilt a Zandi-size K would give (A weights)")
axes[1].axhline(ZANDI_TOP - ZANDI_B80, color=ORANGE, lw=1.2, label="Zandi: +4 pts a year")
axes[0].set_ylabel("top-20 basket minus bottom-80 basket,\nreal growth over 12 months (pts)")
axes[1].set_ylabel("implied top20 - bottom80 gap\n= tilt / kappa (pts a year)")
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{100 * v:+.1f}" if v else "0"))
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{100 * v:+.0f}" if v else "0"))
ylim = np.nanpercentile(np.abs(tm.implied_gap_12m), 97)
axes[1].set_ylim(-1.1 * ylim, 1.1 * ylim)
axes[0].legend(loc="upper left", ncol=3, fontsize=8)
axes[1].legend(loc="upper left", ncol=3, fontsize=8)
axes[0].set_title("Top-tilt index: do the top 20%'s categories outgrow the bottom 80%'s? (fixed base-year baskets, "
                  "12-month real changes)", loc="left", fontsize=10)
axes[1].text(0.0, -0.16, "Shaded: NBER recessions (dark) and calendar 2020 (light). Lower panel clipped at the 97th "
             "percentile of |gap|; the 2020-21 swings run off the scale.\nMonthly A from 2007-01 (2006 bases via "
             "2.4.3U quantity indexes), B from 2015-01 (CE base years 2014-2025).", transform=axes[1].transAxes,
             fontsize=7.5, color=MUTED, va="top")
fig.subplots_adjust(left=0.09, right=0.97, top=0.94, bottom=0.11)
fig.savefig(FIG / "fig_top_tilt.png", dpi=200)
plt.close(fig)

# %% 11. Console summary
# ---------------------------------------------------------------------------------------------------------
# 11. Console summary
# ---------------------------------------------------------------------------------------------------------
pd.set_option("display.width", 200)
print(f"line correspondence 2.3.5 = 2.8.5 (lines 1-22): {LINE_CORR_OK}; eta variant: {ETA_STATUS}")
main = READ[(READ["sample"] == "all") & (READ.theta_role == "main")]
print(main[["window", "source", "spec", "measure", "gap", "ci_lo", "ci_hi", "p_placebo", "p_zandi", "zandi_gap_cum",
            "gap_pa", "r2_fit_vs_flat", "r2_zandi_vs_flat"]].round(4).to_string(index=False))
print(BACKTEST[BACKTEST.spec == "2grp"][["window", "source", "growth_source", "measure", "gap", "gap_actual",
                                         "gap_error", "basket_gap"]].round(4).to_string(index=False))
print(POWER_SUMMARY.round(4).to_string(index=False))
