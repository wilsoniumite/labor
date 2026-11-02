# check_sectors.py — independent checks of the sectors unit (outputs of consumption/recent/code/sectors.py).
#
# Recomputes the key numbers from the tidy data with separate code: the *relative* form of BEA's Fisher
# contributions (sectors.py uses the level form), leaf membership read from the lines file's `path_lines`
# (sectors.py walks parent links), BEA's published tables and the watch page read again from the raw files.
# It then checks the outputs against that recomputation, against BEA's own published numbers, and against the
# identities they must satisfy. Prints one PASS/FAIL line per check and exits 1 if anything fails.
#
# Run from the repo root (after sectors.py):  venv/bin/python -I consumption/recent/checks/check_sectors.py
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                  # consumption/recent/checks
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "code"))       # consumption/code (common.py: paths)
import common                                           # noqa: E402

import json                                             # noqa: E402
import re                                               # noqa: E402
import numpy as np                                      # noqa: E402
import pandas as pd                                     # noqa: E402
import openpyxl                                         # noqa: E402
from tqdm.auto import tqdm                              # noqa: E402

RECENT = HERE.parent
OUT, FIG = RECENT / "out", RECENT / "figures"
TIDY = common.TIDY
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


# %% load
lines = pd.read_csv(TIDY / "bea_pce_u_lines.csv")
u = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", dtype={"table": str, "context": str})
pil = pd.read_csv(TIDY / "bea_pi_long.csv", dtype={"table": str, "context": str})


def wide(df, table, freq):
    x = df[(df["table"] == table) & (df["freq"] == freq)]
    return x.pivot(index="date", columns="line", values="value").sort_index()


V = {f: wide(u, "2.4.5U", f) for f in "MA"}
P = {f: wide(u, "2.4.4U", f) for f in "MA"}
Q = {f: wide(u, "2.4.3U", f) for f in "MA"}
X = {f: wide(u, "2.4.6U", f) for f in "MA"}
PI = {"M": wide(pil, "2.6", "M"), "A": wide(pil, "2.1", "A")}
WINDOWS = [("jobs", "M", "2024-08", "2026-08"), ("12m", "M", "2025-09", "2026-09"), ("6m", "M", "2026-03", "2026-09"),
           ("4y", "M", "2022-09", "2026-09"), ("annual", "A", "2022", "2025")]
groups = {w: pd.read_csv(OUT / f"sector_groups_{a}_{b}.csv") for w, f, a, b in WINDOWS}
contribs = {w: pd.read_csv(OUT / f"sector_contributions_{a}_{b}.csv") for w, f, a, b in WINDOWS}
headline = pd.read_csv(OUT / "headline_sectors.csv")
fin = pd.read_csv(OUT / "care_financing.csv")

# %% A. data and the leaf set
cur = lines[(lines["is_leaf"]) & (lines["last_M_2_4_5U"] == "2026-09")].copy()
LEAVES = cur["line"].astype(int).tolist()
SG = cur.set_index("line")["sign_to_root"].astype(float)
PATH = {int(r.line): set(int(x) for x in str(r.path_lines).split(">")) for r in cur.itertuples()}
check("A1 243 current leaves in the lines file", len(LEAVES) == 243, f"{len(LEAVES)}")
sumgap = (V["M"].loc["2007-01":, LEAVES].mul(SG[LEAVES], axis=1).sum(axis=1) - V["M"].loc["2007-01":, 1]).abs()
check("A2 signed sum of the 243 leaves equals PCE (line 1) every month 2007-01..2026-09, within 11 $mn",
      sumgap.max() <= 11, f"max gap {sumgap.max():.0f} $mn")
check("A3 data run to 2026-09 (monthly) and 2025 (annual)",
      V["M"].index.max() == "2026-09" and V["A"].index.max() == "2025" and X["M"].index.max() == "2026-09")


def members(inc, exc=()):
    return [l for l in LEAVES if (PATH[l] & set(inc)) and not (PATH[l] & set(exc))]


CARE = {"A": [172], "A+": [172, 344, 357], "B": [172, 344, 357, 121, 66, 275],
        "C": [172, 344, 357, 121, 66, 275, 316, 317], "C+": [172, 344, 357, 121, 66, 275, 316, 317, 350, 363],
        "S": [172, 344, 357, 316, 317, 350, 363]}
CARE_LABEL = {"A": "(a) Health care services, households (172)",
              "A+": "(a+) Health care services incl. NPISH health (172 + 344 - 357)",
              "B": "(b) (a+) + medical products, appliances, net health insurance (121, 66, 275)",
              "C": "(c) (b) + child care and social assistance (316, 317)",
              "C+": "(c+) (c) + NPISH social services (350 - 363)",
              "S": "(s) Care services only: (a+) + 316 + 317 + (350 - 363)"}
IMPUTED = [160, 163, 254, 342]


# %% B. independent recomputation: relative form of the Fisher contributions
def relative_pair(v0, v1, r):
    """Relative form: s = quantity relatives implied by values and price relatives r."""
    s = (v1 / v0) / r
    FQ = np.sqrt((v0 * s).sum() / v0.sum() * v1.sum() / (v1 / s).sum())
    FP = np.sqrt((v0 * r).sum() / v0.sum() * v1.sum() / (v1 / r).sum())
    w = v0 * (1 + r / FP)
    return FQ, w * (s - 1) / w.sum(), s


def subset_fisher(v0, v1, s, mask):
    return np.sqrt((v0[mask] * s[mask]).sum() / v0[mask].sum() * v1[mask].sum() / (v1[mask] / s[mask]).sum())


def run(freq, a, b, use_q=False):
    """Monthly (or annual) chain over (a, b]: total growth, leaf window contributions, and relatives of subsets."""
    v_, p_, q_ = V[freq], P[freq], Q[freq]
    dates = [t for t in v_.index if a <= t <= b]
    cum, contrib = 1.0, pd.Series(0.0, index=LEAVES)
    masks = {f"care {k}": np.isin(LEAVES, members(t)) for k, t in CARE.items()}
    masks.update({f"outside {k}": ~np.isin(LEAVES, members(t)) for k, t in CARE.items()})
    masks.update({f"outside {k} imp": ~np.isin(LEAVES, members(t + IMPUTED)) for k, t in CARE.items()})
    rel = {m: 1.0 for m in masks}
    for t0, t1 in zip(dates[:-1], dates[1:]):
        v0 = v_.loc[t0, LEAVES].values * SG[LEAVES].values
        v1 = v_.loc[t1, LEAVES].values * SG[LEAVES].values
        if use_q:                                    # quantity relatives from 2.4.3U, implied price relatives
            sq = q_.loc[t1, LEAVES].values / q_.loc[t0, LEAVES].values
            r = (v1 / v0) / sq
        else:
            r = p_.loc[t1, LEAVES].values / p_.loc[t0, LEAVES].values
        FQ, c, s = relative_pair(v0, v1, r)
        contrib += cum * c
        for m, mk in masks.items():
            rel[m] *= subset_fisher(v0, v1, s, mk)
        cum *= FQ
    return cum - 1, contrib, {m: x - 1 for m, x in rel.items()}


INDEP = {}
for w, f, a, b in tqdm(WINDOWS, desc="independent recomputation"):
    INDEP[w] = run(f, a, b)
for w, f, a, b in WINDOWS:
    tot, con, rel = INDEP[w]
    g = groups[w]
    t_out = g.loc[g.kind == "total", "real_growth_pct"].iloc[0]
    check(f"B1 {w}: leaf-Fisher real growth reproduced by the relative form", abs(100 * tot - t_out) < 1e-6,
          f"{100 * tot:.6f} vs {t_out:.6f} %")
    ct = contribs[w].set_index("line")
    d = (100 * con - ct.loc[LEAVES, "contribution_pp"]).abs().max()
    check(f"B2 {w}: all 243 leaf contributions reproduced", d < 1e-6, f"max |diff| {d:.1e} pp")
    worst = 0.0
    for k in CARE:
        row = g[g.group == CARE_LABEL[k]].iloc[0]
        worst = max(worst, abs(100 * con[members(CARE[k])].sum() - row.contribution_pp),
                    abs(100 * rel[f"care {k}"] - row.real_growth_pct),
                    abs(100 * rel[f"outside {k}"] - g[g.group == f"Outside care {k}"].real_growth_pct.iloc[0]),
                    abs(100 * rel[f"outside {k} imp"]
                        - g[g.group == f"Outside care {k} and imputed items"].real_growth_pct.iloc[0]))
    check(f"B3 {w}: care contributions and care / outside-care / outside-care-and-imputed real growth reproduced "
          "(6 variants)", worst < 1e-6, f"max |diff| {worst:.1e} pp")

# %% C. identities in the output files themselves
for w, f, a, b in WINDOWS:
    ct = contribs[w].set_index("line")
    tot = groups[w].loc[groups[w].kind == "total", "contribution_pp"].iloc[0]
    leafsum = ct.loc[ct.is_leaf, "contribution_pp"].sum()
    check(f"C1 {w}: leaf contributions add to the total and to line 1",
          abs(leafsum - tot) < 1e-9 and abs(ct.loc[1, "contribution_pp"] - tot) < 1e-9,
          f"sum {leafsum:.10f}, total {tot:.10f}")
    kids = ct.dropna(subset=["parent_line"]).groupby("parent_line")["contribution_pp"].sum()
    gap = max(abs(kids[p] - ct.loc[int(p), "contribution_pp"]) for p in kids.index)
    check(f"C2 {w}: every parent's contribution equals the sum of its children's", gap < 1e-9, f"max {gap:.1e}")
    g = groups[w]
    for kind in ["functional", "care-first partition"]:
        gg = g[g.kind == kind]
        s_c, s_n, s_s = gg.contribution_pp.sum(), gg.start_nominal_musd.sum(), gg.share_of_growth_pct.sum()
        n_ok = gg.n_leaves.sum() == 243
        pce0 = g.loc[g.kind == "total", "start_nominal_musd"].iloc[0]
        check(f"C3 {w}: '{kind}' groups partition PCE (243 leaves; contributions, start values, shares add up)",
              n_ok and abs(s_c - tot) < 1e-9 and abs(s_n - pce0) < 1e-3 and abs(s_s - 100) < 1e-9,
              f"n={gg.n_leaves.sum()}, contrib {s_c:.6f} vs {tot:.6f}, shares {s_s:.6f}")
    leaf = ct[ct.is_leaf]
    sets = {k: set(leaf.index[leaf[f"care_{k}"] == "yes"]) for k in CARE}
    nested = sets["A"] <= sets["A+"] <= sets["B"] <= sets["C"] <= sets["C+"] and sets["S"] <= sets["C+"]
    same = all(sets[k] == set(members(CARE[k])) for k in CARE)
    check(f"C4 {w}: care variants nested A < A+ < B < C < C+ and S < C+, and tags match path-based membership",
          nested and same, " ".join(f"{k}:{len(v)}" for k, v in sets.items()))
    one = leaf.func_group.isin([x for x in g[g.kind == "functional"].group]).all()
    check(f"C5 {w}: every leaf carries exactly one functional group", bool(one))

# %% D. against BEA's own numbers
for w, f, a, b in WINDOWS:
    g = groups[w]
    res = g.loc[g.kind == "residual", "real_growth_pct"].iloc[0]
    bea = 100 * (X[f].loc[b, 1] / X[f].loc[a, 1] - 1)
    tol = 0.001 if f == "A" else 0.03
    check(f"D1 {w}: residual BEA real PCE minus leaf Fisher is small (|r| <= {tol} pp)",
          abs(res) <= tol and abs(g.loc[g.kind == "bea", "real_growth_pct"].iloc[0] - bea) < 1e-9,
          f"BEA {bea:.4f}%, residual {res:+.4f} pp")
major = pd.read_csv(TIDY / "bea_pce_major_long.csv", dtype={"table": str, "context": str})
x286 = major[(major["table"] == "2.8.6") & (major["line"] == 1)].set_index("date")["value"]
ends = [t for w, f, a, b in WINDOWS if f == "M" for t in (a, b)]
check("D1b BEA's Table 2.8.6 real PCE equals 2.4.6U line 1 at every monthly window endpoint",
      all(x286[t] == X["M"].loc[t, 1] for t in ends), f"{len(ends)} endpoints")
ann = []
for y0, y1 in zip([str(y) for y in range(2007, 2025)], [str(y) for y in range(2008, 2026)]):
    tot, _, _ = run("A", y0, y1)
    ann.append(100 * tot - 100 * (X["A"].loc[y1, 1] / X["A"].loc[y0, 1] - 1))
check("D2 annual leaf Fisher equals BEA's annual real PCE growth in every year 2008-2025 (|diff| <= 0.001 pp)",
      max(map(abs, ann)) <= 0.001, f"max |diff| {max(map(abs, ann)):.5f} pp")
comp = pd.read_csv(OUT / "published_comparison.csv", dtype={"period": str})
for tb, tol in [("T20302-A", 0.0056), ("T20402-A", 0.0056), ("T20802-M", 0.0100)]:
    x = comp[comp.table == tb]
    check(f"D3 {tb}: our contributions match BEA's published ones within rounding (|diff| <= {tol} pp)",
          len(x) > 0 and x.diff_pp.abs().max() <= tol,
          f"{len(x)} line-periods, max |diff| {x.diff_pp.abs().max():.4f}")
# an independent read of the published monthly health care contributions (Table 2.8.2 line 16)
wb = openpyxl.load_workbook(common.RAW / "bea/nipa/xls_survey/Section2All_xls.xlsx", read_only=True, data_only=True)
rows = list(wb["T20802-M"].iter_rows(values_only=True))
hdr = [str(h) for h in rows[7]]
hl = [r for r in rows if r[0] is not None and str(r[0]).strip() == "16"][0]
assert "Health care" in str(hl[1])
pub = pd.Series([float(x) for x in hl[3:]], index=[h.replace("M", "-") for h in hdr[3:]])
ours = []
for t0, t1 in zip(V["M"].loc["2021-12":].index[:-1], V["M"].loc["2021-12":].index[1:]):
    v0 = V["M"].loc[t0, LEAVES].values * SG[LEAVES].values
    v1 = V["M"].loc[t1, LEAVES].values * SG[LEAVES].values
    _, c, _ = relative_pair(v0, v1, P["M"].loc[t1, LEAVES].values / P["M"].loc[t0, LEAVES].values)
    ours.append((t1, 100 * c[np.isin(LEAVES, members([172]))].sum()))
dd = max(abs(v - pub[t]) for t, v in ours)
check("D4 health care (172) monthly contributions 2022-01..2026-09 match Table 2.8.2 line 16 (|diff| <= 0.006 pp)",
      dd <= 0.006, f"max |diff| {dd:.4f} pp over {len(ours)} months")
for w, f, a, b in WINDOWS:
    ct = contribs[w].set_index("line")
    nonleaf = ct[(~ct.is_leaf) & (~ct.index.isin([145, 333]))]
    dn = (nonleaf.real_growth_pct - nonleaf.real_growth_pct_bea_2_4_3U).abs()
    care_tops = [172, 121, 66, 275, 316, 317, 344, 357, 350, 363]
    dc = (ct.loc[care_tops, "real_growth_pct"] - ct.loc[care_tops, "real_growth_pct_bea_2_4_3U"]).abs().max()
    if f == "A":
        check(f"D5 {w}: own Fisher growth of every parent line equals BEA's 2.4.3U index growth (|diff| <= 0.01 pp)",
              dn.max() <= 0.01, f"max |diff| {dn.max():.4f} pp over {len(dn)} lines")
    else:
        check(f"D5 {w}: own Fisher growth of the care lines matches BEA's 2.4.3U indexes (|diff| <= 0.1 pp)",
              dc <= 0.1, f"care lines max |diff| {dc:.4f} pp; all parents max {dn.max():.3f} pp "
              "(monthly detail indexes carry BEA's temporal adjustment)")

# %% E. headline numbers: the watch figures, the headline file, the jobs side
g6 = 100 * (X["M"].loc["2026-09", 1] / X["M"].loc["2026-03", 1] - 1)
p6 = 100 * (PI["M"].loc["2026-09", 36] / PI["M"].loc["2026-03", 36] - 1)
g12 = 100 * (X["M"].loc["2026-09", 1] / X["M"].loc["2025-09", 1] - 1)
p12 = 100 * (PI["M"].loc["2026-09", 36] / PI["M"].loc["2025-09", 36] - 1)
check("E1 watch numbers: real PCE +1.82% and real income excl. transfers +0.05% over six months to Sep 2026; "
      "+2.54% and +0.54% over twelve; saving rate 3.8%",
      (round(g6, 2), round(p6, 2), round(g12, 2), round(p12, 2), PI["M"].loc["2026-09", 35]) ==
      (1.82, 0.05, 2.54, 0.54, 3.8), f"{g6:.3f} {p6:.3f} {g12:.3f} {p12:.3f} {PI['M'].loc['2026-09', 35]}")
worst = 0.0
for w, f, a, b in WINDOWS:
    tot, con, rel = INDEP[w]
    pce0 = V[f].loc[a, 1]        # shares of level are of published PCE (line 1); the leaves sum to it within $11mn
    for k in CARE:
        h = headline[(headline.window == w) & (headline.care_variant == k)].iloc[0]
        ms = members(CARE[k])
        lvl = 100 * (V[f].loc[a, ms] * SG[ms]).sum() / pce0
        nom_inc = 100 * ((V[f].loc[b, ms] * SG[ms]).sum() - (V[f].loc[a, ms] * SG[ms]).sum()) / (
            V[f].loc[b, 1] - V[f].loc[a, 1])
        care_px = 100 * ((V[f].loc[b, ms] * SG[ms]).sum() / (V[f].loc[a, ms] * SG[ms]).sum()
                         / (1 + rel[f"care {k}"]) - 1)
        worst = max(worst, abs(lvl - h.care_start_share_of_pce_pct),
                    abs(nom_inc - h.care_share_of_nominal_increase_pct),
                    abs(care_px - h.care_implicit_price_change_pct),
                    abs(100 * con[ms].sum() / tot - h.care_share_of_growth_pct),
                    abs(100 * rel[f"outside {k}"] - h.outside_care_real_growth_pct),
                    abs(100 * (X[f].loc[b, 1] / X[f].loc[a, 1] - 1) - h.real_pce_growth_pct_bea),
                    abs(100 * (PI[f].loc[b, 36] / PI[f].loc[a, 36] - 1) - h.real_pi_ex_transfers_growth_pct))
check("E2 headline file: care share of level, share of growth, outside-care growth, real PCE and real income "
      "growth reproduced for every window and variant", worst < 1e-6, f"max |diff| {worst:.1e}")
html = (common.RAW / "watch" / "jobs-outside-care.html").read_text(encoding="utf-8")
data = json.loads(re.search(r'id="plot-1">(.*?)</script>', html, re.S).group(1))
J = {s["name"]: dict(s["points"]) for s in data["series"]}
k12 = (J["Private jobs outside care"]["2026-09-01"], J["Health care and social assistance"]["2026-09-01"],
       J["Government"]["2026-09-01"])
two = {n: J[n]["2026-08-01"] + J[n]["2025-08-01"] for n in J}
share2 = 100 * two["Health care and social assistance"] / sum(two.values())
jw = pd.read_csv(OUT / "jobs_watch_windows.csv").set_index("window")
check("E3 jobs from the vendored watch page: +192k / +520k / -216k over the year to Sep 2026; care 107% of net job "
      "growth Aug 2024 - Aug 2026",
      k12 == (192.0, 520.0, -216.0) and round(share2) == 107
      and abs(jw.loc["jobs", "care_share_of_net_job_growth_pct"] - share2) < 1e-9, f"{k12}, {share2:.2f}%")

hist = pd.read_csv(OUT / "care_share_history.csv", dtype={"period": str}).set_index("period")
worst = 0.0
for per_, f, a, b in [("2015-09 to 2019-09", "M", "2015-09", "2019-09"), ("2018-09 to 2022-09", "M", "2018-09", "2022-09"),
                      ("2015 to 2019", "A", "2015", "2019"), ("2010 to 2019", "A", "2010", "2019")] + \
        [(str(y), "A", str(y - 1), str(y)) for y in range(2011, 2026)]:
    tot, con, rel = run(f, a, b)
    for k in ["A+", "B", "C"]:
        ms = members(CARE[k])
        worst = max(worst, abs(100 * con[ms].sum() / tot - hist.loc[per_, f"care_{k}_share_of_growth_pct"]),
                    abs(100 * (V[f].loc[a, ms] * SG[ms]).sum() / V[f].loc[a, 1]
                        - hist.loc[per_, f"care_{k}_share_of_level_pct"]),
                    abs(100 * rel[f"outside {k}"] - hist.loc[per_, f"outside_care_{k}_real_growth_pct"]))
check("E4 context: care shares of growth and level and outside-care growth reproduced for every year 2011-2025 and "
      "for the pre-pandemic windows", worst < 1e-6, f"max |diff| {worst:.1e}")
pre = {n: sum(J[n][f"{y}-09-01"] for y in range(2016, 2020)) for n in J}
pre_share = 100 * pre["Health care and social assistance"] / sum(pre.values())
check("E5 jobs, four years to Sep 2019: care share of net job growth from the watch page",
      abs(jw.loc["pre4y", "care_share_of_net_job_growth_pct"] - pre_share) < 1e-9, f"{pre_share:.2f}%")
# the page's latest two years (Sep 2024 - Sep 2026) beside the jobs window: jobs from the raw page, spending recomputed
jcw = pd.read_csv(OUT / "jobs_windows_compare.csv").set_index("window")
two_s = {n: J[n]["2026-09-01"] + J[n]["2025-09-01"] for n in J}
share_s = 100 * two_s["Health care and social assistance"] / sum(two_s.values())
tot_s, con_s, rel_s = run("M", "2024-09", "2026-09")
mcs = members(CARE["C"])
rs, ra = jcw.loc["jobs_latest"], jcw.loc["jobs"]
hj = headline[(headline.window == "jobs") & (headline.care_variant == "C")].iloc[0]
worst = max(abs(share_s - rs.care_share_of_net_job_growth_pct), abs(100 * tot_s - rs.real_pce_growth_pct_leaf),
            abs(100 * con_s[mcs].sum() / tot_s - rs.care_C_share_of_real_growth_pct),
            abs(100 * rel_s["care C"] - rs.care_C_real_growth_pct),
            abs(100 * rel_s["outside C"] - rs.outside_care_C_real_growth_pct),
            abs(100 * (X["M"].loc["2026-09", 1] / X["M"].loc["2024-09", 1] - 1) - rs.real_pce_growth_pct_bea),
            abs(100 * (PI["M"].loc["2026-09", 36] / PI["M"].loc["2024-09", 36] - 1) - rs.real_pi_ex_transfers_growth_pct),
            abs(ra.care_share_of_net_job_growth_pct - jw.loc["jobs", "care_share_of_net_job_growth_pct"]),
            abs(ra.care_C_share_of_real_growth_pct - hj.care_share_of_growth_pct),
            abs(ra.outside_care_C_real_growth_pct - hj.outside_care_real_growth_pct))
check("E6 jobs window against the page's latest two years: Sep 2024 - Sep 2026 jobs -31k / +1,285k / -122k (113.5%) "
      "from the raw page, and care (c)'s share of real PCE growth and outside-care growth over the same months "
      "recomputed; the Aug 2024 - Aug 2026 row agrees with the main tables",
      (two_s["Private jobs outside care"], two_s["Health care and social assistance"], two_s["Government"])
      == (-31.0, 1285.0, -122.0) and round(share_s, 1) == 113.5 and worst < 1e-6,
      f"{share_s:.2f}%; care share of real growth {100 * con_s[mcs].sum() / tot_s:.2f}%, outside care "
      f"{100 * rel_s['outside C']:.2f}%; max |diff| {worst:.1e}")

# %% F. financing identities
for w, f, a, b in WINDOWS:
    x = fin[(fin.window == w) & (fin.block == "bridge")].set_index("item")["increment_musd"]
    pub_d = V[f].loc[b, 1] - V[f].loc[a, 1]
    gapb = abs(x["= Change in PCE (sum of the above)"] - pub_d)
    check(f"F1 {w}: income, transfers, taxes, interest and saving bridge to the change in PCE (within 4 $mn)",
          gapb <= 4, f"bridge {x['= Change in PCE (sum of the above)']:.0f} vs dPCE {pub_d:.0f} $mn")
    # gap decomposition identity: g_C - g_Y = s_M (g_M - g_Y) + (1 - s_M)(g_R - g_Y), and the M share recomputed
    y0 = PI[f].loc[a, 1] - PI[f].loc[a, 16]
    y1 = PI[f].loc[b, 1] - PI[f].loc[b, 16]
    c0, c1 = V[f].loc[a, 1], V[f].loc[b, 1]
    m0 = PI[f].loc[a, 19] + PI[f].loc[a, 20]
    m1 = PI[f].loc[b, 19] + PI[f].loc[b, 20]
    gY, gC, gM = y1 / y0 - 1, c1 / c0 - 1, m1 / m0 - 1
    gR = (c1 - m1) / (c0 - m0) - 1
    ident = (m0 / c0) * (gM - gY) + (1 - m0 / c0) * (gR - gY) - (gC - gY)
    gx = fin[(fin.window == w) & (fin.block == "gap")].set_index("item")["value"]
    mpart = gx["Part of nominal gap from Medicare + Medicaid (19 + 20): s0 (g - gY), pp"]
    ok = abs(ident) < 1e-12 and abs(100 * (m0 / c0) * (gM - gY) - mpart) < 1e-9
    if gC - gY > 0.0025:
        ok = ok and abs(100 * (m0 / c0) * (gM - gY) / (gC - gY)
                        - gx["Share of the nominal gap from Medicare + Medicaid (19 + 20), %"]) < 1e-6
    else:
        ok = ok and pd.isna(gx["Share of the nominal gap from Medicare + Medicaid (19 + 20), %"])
    check(f"F2 {w}: gap decomposition identity holds and the Medicare + Medicaid part is reproduced", ok,
          f"nominal gap {100 * (gC - gY):.3f} pp, M+M part {100 * (m0 / c0) * (gM - gY):.3f} pp")

# %% G. notes and figures
notes = (RECENT / "NOTES_sectors.md")
tab = (OUT / "notes_tables_sectors.md").read_text(encoding="utf-8")
tlines = [l for l in tab.splitlines() if l.startswith("|")]
missing = [l for l in tlines if notes.exists() and l not in notes.read_text(encoding="utf-8")]
check("G1 every results-table line in out/notes_tables_sectors.md appears verbatim in NOTES_sectors.md",
      notes.exists() and not missing, f"{len(tlines)} lines, {len(missing)} missing")
gen = re.split(r"<!-- ([\w-]+) -->\n", (OUT / "notes_text_sectors.md").read_text(encoding="utf-8"))[1:]
passages = dict(zip(gen[0::2], gen[1::2]))
flat = lambda s: re.sub(r"\s+", " ", s).strip()                                               # noqa: E731
flat_notes = flat(notes.read_text(encoding="utf-8")) if notes.exists() else ""
gmiss = [k for k, s in passages.items() if flat(s) not in flat_notes]
check("G3 every generated passage in out/notes_text_sectors.md (prose whose numbers are read from the CSVs) appears in "
      "NOTES_sectors.md, line wrapping aside", len(passages) >= 10 and not gmiss,
      f"{len(passages)} passages, missing: {gmiss}")
from PIL import Image                                    # noqa: E402  (matplotlib's own dependency)
figs = ["fig_care_share_of_growth.png", "fig_outside_care.png", "fig_contributions_2024-08_2026-08.png",
        "fig_contributions_2022-09_2026-09.png"]
dpis = {}
for fn in figs:
    p = FIG / fn
    dpis[fn] = round(Image.open(p).info.get("dpi", (0, 0))[0]) if p.exists() else None
check("G2 the four figures exist and are saved at 200 dpi", all(v == 200 for v in dpis.values()), str(dpis))

# %% H. sensitivity: quantity relatives from 2.4.3U instead of price relatives from 2.4.4U
worst = []
for w, f, a, b in WINDOWS:
    totq, conq, _ = run(f, a, b, use_q=True)
    tot, con, _ = INDEP[w]
    mc = members(CARE["C"])
    worst.append((w, 100 * (totq - tot), 100 * (conq[mc].sum() - con[mc].sum())))
mx = max(max(abs(t), abs(c)) for _, t, c in worst)
check("H1 using 2.4.3U quantity relatives instead of 2.4.4U prices moves totals and the care (c) contribution by "
      "at most 0.02 pp", mx <= 0.02, "; ".join(f"{w}: total {t:+.4f}, care {c:+.4f}" for w, t, c in worst))

# %% I. care in dollars, when the gap opened, Table 4's BEA columns, leaf v/p against 2.4.3U (recomputed here with the
# relative form and path-based membership)
DW = WINDOWS + [("pre4y", "M", "2015-09", "2019-09"), ("covid4y", "M", "2018-09", "2022-09"),
                ("7y", "M", "2019-09", "2026-09")]
ds = pd.read_csv(OUT / "care_dollar_shares.csv").set_index(["window", "care_variant"])
worst, n = 0.0, 0
for w, f, a, b in DW:
    tot, con, rel = INDEP[w] if w in INDEP else run(f, a, b)
    p0, p1 = V[f].loc[a, 1], V[f].loc[b, 1]
    px = (p1 / p0) / (X[f].loc[b, 1] / X[f].loc[a, 1]) - 1
    for k in CARE:
        ms = members(CARE[k])
        c0, c1 = (V[f].loc[a, ms] * SG[ms]).sum(), (V[f].loc[b, ms] * SG[ms]).sum()
        g = rel[f"care {k}"]
        c1eq = c0 * (1 + g) * (1 + px)
        mine = {"start_share_of_pce_pct": 100 * c0 / p0, "end_share_of_pce_pct": 100 * c1 / p1,
                "end_share_at_start_prices_pct": 100 * c0 / p0 * (1 + g) / (1 + tot),
                "share_of_real_growth_pct": 100 * con[ms].sum() / tot,
                "share_of_nominal_increase_pct": 100 * (c1 - c0) / (p1 - p0),
                "share_of_nominal_increase_if_care_prices_as_pce_pct": 100 * (c1eq - c0) / (p1 - p0 + c1eq - c1)}
        mine["of_which_general_inflation_pp"] = (mine["share_of_real_growth_pct"]
                                                 - mine["share_of_nominal_increase_if_care_prices_as_pce_pct"])
        mine["of_which_relative_prices_pp"] = (mine["share_of_nominal_increase_if_care_prices_as_pce_pct"]
                                               - mine["share_of_nominal_increase_pct"])
        r = ds.loc[(w, k)]
        worst = max([worst] + [abs(v - r[c]) for c, v in mine.items()])
        worst = max(worst, abs(r.real_minus_nominal_share_pp - r.of_which_general_inflation_pp
                               - r.of_which_relative_prices_pp))
        n += 1
r4 = ds.loc[("4y", "C")]
check("I1 care in dollars: shares of the level at both ends (current dollars and start-of-window prices), shares of "
      "real growth and of the dollar increase, and the inflation / relative-price split, every window and variant",
      worst < 1e-6 and n == len(ds), f"{n} rows, max |diff| {worst:.1e}; 4y (c): {r4.start_share_of_pce_pct:.2f} -> "
      f"{r4.end_share_of_pce_pct:.2f} ($), -> {r4.end_share_at_start_prices_pct:.2f} (volumes); split "
      f"{r4.of_which_general_inflation_pp:.2f} + {r4.of_which_relative_prices_pp:.2f}")
gtm = pd.read_csv(OUT / "gap_timing.csv").set_index("period")
worst = 0.0
mc = members(CARE["C"])
# the month in which income's lead over spending, measured from Sep 2022, was largest: the base of the 'low' rows
cum_gap = (X["M"].loc["2022-09":, 1] / X["M"].loc["2022-09", 1] - PI["M"].loc["2022-09":, 36] / PI["M"].loc["2022-09", 36])
LOW = cum_gap.idxmin()
GAP_ROWS = [("pre", "2022-09", "2026-03"), ("6m", "2026-03", "2026-09"), ("4y", "2022-09", "2026-09"),
            ("12m", "2025-09", "2026-09"), ("low_pre", LOW, "2026-03"), ("low", LOW, "2026-09")]
for p, a, b in GAP_ROWS:
    tot, con, rel = run("M", a, b)
    p0, p1 = V["M"].loc[a, 1], V["M"].loc[b, 1]
    c0, c1 = (V["M"].loc[a, mc] * SG[mc]).sum(), (V["M"].loc[b, mc] * SG[mc]).sum()
    gyr = PI["M"].loc[b, 36] / PI["M"].loc[a, 36] - 1
    gY = (PI["M"].loc[b, 1] - PI["M"].loc[b, 16]) / (PI["M"].loc[a, 1] - PI["M"].loc[a, 16]) - 1
    gx = X["M"].loc[b, 1] / X["M"].loc[a, 1] - 1
    care_r, care_n = con[mc].sum() - c0 / p0 * gyr, c0 / p0 * (c1 / c0 - 1 - gY)
    r = gtm.loc[p]
    worst = max(worst, abs(100 * (gx - gyr) - r.real_gap_pp_bea), abs(100 * (tot - gyr) - r.real_gap_pp_leaf),
                abs(100 * care_r - r.care_C_part_of_real_gap_pp),
                abs(100 * (tot - gyr - care_r) - r.outside_care_C_part_of_real_gap_pp),
                abs(100 * (p1 / p0 - 1 - gY) - r.nominal_gap_pp), abs(100 * care_n - r.care_C_part_of_nominal_gap_pp),
                abs(100 * (p1 / p0 - 1 - gY - care_n) - r.outside_care_C_part_of_nominal_gap_pp))
    if p != "pre":                               # shares are left blank where the gap is not clearly positive
        worst = max(worst, abs(100 * care_r / (tot - gyr) - r.care_C_share_of_real_gap_pct),
                    abs(100 * care_n / (p1 / p0 - 1 - gY) - r.care_C_share_of_nominal_gap_pct))
    if r.start != a or r.end != b:
        worst = np.inf
g9 = fin[(fin.block == "gap")].set_index(["window", "item"])["value"]
lab_c = CARE_LABEL["C"]
same = all(abs(gtm.loc[p, "care_C_share_of_real_gap_pct"]
               - g9[(w, f"Share of the real gap from {lab_c}, % (gap on the leaf Fisher)")]) < 1e-9
           and abs(gtm.loc[p, "care_C_share_of_nominal_gap_pct"] - g9[(w, f"Share of the nominal gap from {lab_c}, %")])
           < 1e-9 for p, w in [("6m", "6m"), ("4y", "4y"), ("12m", "12m")])
check("I2 when the gap opened and how its split depends on the starting month: real and nominal gaps, their care (c) / "
      "outside-care parts and care's shares from Sep 2022 (to Mar and Sep 2026), from the month of income's largest "
      "lead (found here: Jan 2024) and over twelve and six months reproduced; the 6m, 12m and 4y rows agree with "
      "care_financing.csv",
      worst < 1e-6 and same and pd.isna(gtm.loc["pre", "care_C_share_of_real_gap_pct"]) and LOW == "2024-01"
      and len(gtm) == len(GAP_ROWS),
      f"max |diff| {worst:.1e} pp; low month {LOW} ({100 * cum_gap.min():+.2f} pt); care's share of the real / nominal "
      "gap: " + ", ".join(f"{p} {gtm.loc[p, 'care_C_share_of_real_gap_pct']:.1f} / "
                          f"{gtm.loc[p, 'care_C_share_of_nominal_gap_pct']:.1f}" for p, _, _ in GAP_ROWS[1:]))
# the indexes behind the gap path quoted in the notes (outside_care_monthly.csv), recomputed from the raw tables
mon = pd.read_csv(OUT / "outside_care_monthly.csv").pivot(index="date", columns="series", values="index_2022_09_100")
ix_x = 100 * X["M"].loc["2007-01":, 1] / X["M"].loc["2022-09", 1]
ix_y = 100 * PI["M"].loc["2007-01":, 36] / PI["M"].loc["2022-09", 36]
dmon = max((mon["real_pce_bea"] - ix_x).abs().max(), (mon["real_pi_ex_transfers"] - ix_y).abs().max())
from_low = 100 * (X["M"].loc[LOW:, 1] / X["M"].loc[LOW, 1] - PI["M"].loc[LOW:, 36] / PI["M"].loc[LOW, 36])
check("I6 the gap path: BEA real PCE and real income excl. transfers indexed to Sep 2022 in outside_care_monthly.csv "
      "reproduced; measured from Jan 2024 the gap was about 2 points by Dec 2024 and 4.2 by Sep 2026",
      dmon < 1e-9 and round(from_low["2024-12"], 1) == 2.0 and round(from_low["2026-09"], 1) == 4.2,
      f"max |diff| {dmon:.1e}; from {LOW}: Dec 2024 {from_low['2024-12']:.2f}, Jan 2025-Mar 2026 "
      f"{from_low.loc['2025-01':'2026-03'].min():.2f} to {from_low.loc['2025-01':'2026-03'].max():.2f}, Sep 2026 "
      f"{from_low['2026-09']:.2f} pt")
# care (c) by the indicator behind the advance estimate (Handbook Tables 5.A and 5.B), path-based membership
adv = pd.read_csv(OUT / "care_advance_sources.csv").set_index("group")
ADV = {"CES employment, hours and earnings": [176, 183, 187, 317, 344, 357], "Judgmental trend": [174, 316, 275],
       "Monthly retail sales (Census MRTS)": [121, 66], "Dental patient volumes (American Dental Association)": [175],
       "Care (c)": CARE["C"]}
parts_ = [members(t) for g, t in ADV.items() if g != "Care (c)"]
partition_ok = sorted(sum(parts_, [])) == sorted(mc) and len(set(sum(parts_, []))) == len(mc)
_, con_q3, _ = run("M", "2026-06", "2026-09")
_, con_6m, _ = run("M", "2026-03", "2026-09")
lvl_ = lambda ms: (V["M"].loc["2026-09", ms] * SG[ms]).sum()                                   # noqa: E731
worst = 0.0
for g, tops in ADV.items():
    ms, r = members(tops), adv.loc[g]
    worst = max(worst, abs(100 * lvl_(ms) / lvl_(mc) - r.share_of_care_C_2026_09_pct),
                abs(100 * con_q3[ms].sum() - r.contribution_q3_pp), abs(100 * con_6m[ms].sum() - r.contribution_6m_pp),
                abs(100 * con_q3[ms].sum() / con_q3[mc].sum() - r.share_of_care_C_contribution_q3_pct),
                abs(100 * con_6m[ms].sum() / con_6m[mc].sum() - r.share_of_care_C_contribution_6m_pct))
ces = adv.loc["CES employment, hours and earnings"]
check("I5 care (c) by advance-estimate indicator: the four groups partition care (c); their shares of care spending in "
      "Sep 2026 and their contributions in Jul-Sep 2026 and over the watch window reproduced",
      partition_ok and worst < 1e-6 and len(adv) == len(ADV),
      f"max |diff| {worst:.1e}; CES-based {ces.share_of_care_C_2026_09_pct:.1f}% of care, {ces.contribution_q3_pp:.3f} "
      f"of {adv.loc['Care (c)', 'contribution_q3_pp']:.3f} pp in Jul-Sep")
hbe = pd.read_csv(OUT / "care_share_history_bea.csv", dtype={"period": str}).set_index("period")
worst, n = 0.0, 0
for per_, f, a, b in [("2015-09 to 2019-09", "M", "2015-09", "2019-09"), ("2018-09 to 2022-09", "M", "2018-09", "2022-09"),
                      ("2022-09 to 2026-09", "M", "2022-09", "2026-09"), ("2015 to 2019", "A", "2015", "2019"),
                      ("2010 to 2019", "A", "2010", "2019")] + [(str(y), "A", str(y - 1), str(y))
                                                               for y in range(2008, 2026)]:
    tot, con, rel = run(f, a, b)
    bea = X[f].loc[b, 1] / X[f].loc[a, 1] - 1
    r = hbe.loc[per_]
    worst = max(worst, abs(100 * bea - r.real_pce_growth_pct_bea), abs(100 * (bea - tot) - r.residual_pp),
                abs(100 * con[members(CARE["C"])].sum() / bea - r.care_C_share_of_bea_growth_pct))
    n += 1
check("I3 Table 4's BEA columns: BEA real PCE growth, the residual and care (c)'s share of BEA's growth reproduced for "
      "every year 2008-2025 and the five spans", worst < 1e-6, f"{n} periods, max |diff| {worst:.1e}; residual "
      f"2018-09..2022-09 {hbe.loc['2018-09 to 2022-09', 'residual_pp']:+.3f} pp")
vq = pd.read_csv(OUT / "leaf_vp_vs_q.csv")
best = (0.0, None, None)
dates = V["M"].index.tolist()
for t0, t1 in zip(dates[:-1], dates[1:]):
    if t1 < "2022-01":
        continue
    implied = (V["M"].loc[t1, LEAVES] / V["M"].loc[t0, LEAVES]) / (P["M"].loc[t1, LEAVES] / P["M"].loc[t0, LEAVES])
    gap = (implied / (Q["M"].loc[t1, LEAVES] / Q["M"].loc[t0, LEAVES]) - 1).abs()
    if gap.max() > best[0]:
        best = (gap.max(), int(gap.idxmax()), t1)
top = vq.iloc[0]
check("I4 leaves: the largest monthly gap since 2022-01 between the 2.4.5U / 2.4.4U quantity relative and 2.4.3U's",
      abs(100 * best[0] - top.max_gap_pct_monthly_since_2022_01) < 1e-9 and best[1] == top.line
      and best[2] == top.month_of_max_since_2022_01, f"{100 * best[0]:.3f}% (line {best[1]}, {best[2]})")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{len(RESULTS) - n_fail} PASS, {n_fail} FAIL")
sys.exit(1 if n_fail else 0)
