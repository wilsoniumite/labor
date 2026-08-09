# build_wedges.py — unit 4: family C, the wedge layer (spec:
# companion_schedule_spec.md). Locates the deflation that turns rho into
# rho-tilde and runs the targeting-order TEST — Proposition 2's signature
# that demolition consumes high-wedge tasks first. The direction is a
# hypothesis under test: construction is gated in checks, the RESULT is
# reported whichever way it lands.
#
# Wedge measures per occ1990dd:
#   union_cov_9901 / union_mem_9901 — Hirsch-Macpherson (unionstats.com)
#     coverage/membership shares by 1990-basis census occupation, averaged
#     1999-2001 (the PRE-period wedge: measured at the panel base, before
#     any flip in the window — no reverse causation from later demolition).
#   union_cov_2025 — same source, 2025 file (2018-census codes chained
#     census2018 -> SOC2018 -> occ1990dd).
#   licensed_2025 — CPS table 53 licensed-or-certified share, published at
#     ~22 broad CPS groups = SOC major groups; attached to detailed
#     occupations by each occupation's employment mix over SOC majors.
#     ECOLOGICAL ATTACHMENT, labeled: group-level shares said of detailed
#     occupations — resolution the public data allows, stated not hidden.
#   Wedge-rent magnitude: A&R (2026) published estimate (rents 40-50%
#   above base for automated jobs; The Link, Figure 4) is the LEVEL anchor,
#   cited not re-derived; no per-occupation mu is constructed here.
#
# The tests (all employment-weighted, banded across the three flip rules):
#   T1 targeting order: pre-period union coverage by flip cohort
#      (2000-07, 2008-15, 2016-25) among flipped occupations + Spearman
#      (flip year vs pre-period coverage). Prop 2 predicts early cohorts
#      carry more wedge.
#   T2 conditional version: same within routine-intensity terciles (the
#      automatability control the spec pre-registered).
#   T3 fortification glance: licensed_2025 and union coverage of survivors
#      vs flipped — quantity-form protection should sit with survivors.
import io
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "figures"))
sys.path.insert(0, HERE)
from fetch import fetch  # noqa: E402
import build_panel as bp  # noqa: E402

RULES = ["d30", "d40", "d50"]
COHORTS = [(2000, 2007, "2000-07"), (2008, 2015, "2008-15"),
           (2016, 2025, "2016-25")]
MIN_COHORT_N = 10
# CPS certification table 53 group names -> SOC major codes (published
# correspondence, mechanical; hand-verified against the table 2026-08-06)
CPS_GROUP_SOC = {
    "Management occupations": "11",
    "Business and financial operations occupations": "13",
    "Computer and mathematical occupations": "15",
    "Architecture and engineering occupations": "17",
    "Life, physical, and social science occupations": "19",
    "Community and social services occupations": "21",
    "Legal occupations": "23",
    "Education, training, and library occupations": "25",
    "Arts, design, entertainment, sports, and media occupations": "27",
    "Healthcare practitioners and technical occupations": "29",
    "Healthcare support occupations": "31",
    "Protective service occupations": "33",
    "Food preparation and serving related occupations": "35",
    "Building and grounds cleaning and maintenance occupations": "37",
    "Personal care and service occupations": "39",
    "Sales and related occupations": "41",
    "Office and administrative support occupations": "43",
    "Farming, fishing, and forestry occupations": "45",
    "Construction and extraction occupations": "47",
    "Installation, maintenance, and repair occupations": "49",
    "Production occupations": "51",
    "Transportation and material moving occupations": "53",
}

ledger = []


def note(msg):
    ledger.append(msg)
    print(msg)


# ------------------------------------------------------------- union files
def read_unionstats(year):
    """-> DataFrame [coc(str), emp, mem_share, cov_share] (detail rows)."""
    raw = pd.read_excel(fetch(f"unionstats_occ_{year}.xlsx"), header=None)
    hdr = next(i for i in range(10)
               if str(raw.iloc[i, 0]).strip().upper() == "COC")
    df = raw.iloc[hdr + 1:, :8].copy()
    df.columns = ["coc", "occupation", "obs", "emp", "mem", "cov",
                  "mem_share", "cov_share"]
    df["coc"] = pd.to_numeric(df["coc"], errors="coerce")
    df = df.dropna(subset=["coc"])                 # group rows carry no code
    for c in ["emp", "mem_share", "cov_share"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["emp", "cov_share"])
    df["coc"] = df["coc"].astype(int).astype(str)
    note(f"unionstats {year}: {len(df)} detail occupations, "
         f"{df['emp'].sum():,.0f}k employment")
    return df


def occ1990_dd_map():
    dd = bp.read_dta("occ1990_occ1990dd.zip", "occ1990_occ1990dd.dta")
    dd = dd.dropna()
    return {str(int(o)): int(d) for o, d in dd.itertuples(index=False)}


def cen2018_soc_pairs():
    """census2018 4-digit -> SOC2018 codes, from the 2018 code list."""
    raw, hdr = bp._header_scan(fetch("2018-occupation-code-list-and-crosswalk.xlsx"),
                               "2018 Census Occ Code List", "2018 Census Code")
    cols = {j: str(raw.iloc[hdr, j]).strip().lower() for j in range(raw.shape[1])}
    cen_col = next(j for j, v in cols.items() if "census code" in v)
    soc_col = next(j for j, v in cols.items() if "soc" in v and "code" in v)
    pairs = []
    for i in range(hdr + 1, len(raw)):
        cen = str(raw.iloc[i, cen_col]).strip().split(".")[0]
        if not re.match(r"^\d{1,4}$", cen):
            continue
        for soc in re.findall(r"\d{2}-\d{4}", str(raw.iloc[i, soc_col])):
            pairs.append((f"{int(cen):04d}", soc))
        for wild in bp.WILD_RE.findall(str(raw.iloc[i, soc_col])):
            pairs.append((f"{int(cen):04d}", wild.rstrip("X")))
    return pairs


def union_to_dd(df, year, chains):
    """Map a unionstats frame to occ1990dd (employment-weighted shares)."""
    rows = []
    if year <= 2002:                               # 1990-basis codes, direct
        m = occ1990_dd_map()
        for r in df.itertuples(index=False):
            dd = m.get(r.coc)
            if dd is not None:
                rows.append((dd, r.emp, r.mem_share, r.cov_share))
    else:                                          # 2018 census -> SOC -> dd
        pairs = {}
        for cen, soc in cen2018_soc_pairs():
            pairs.setdefault(cen, []).append(soc)
        for r in df.itertuples(index=False):
            socs = pairs.get(f"{int(r.coc):04d}", [])
            dds = set()
            for soc in socs:
                if soc.endswith("-") or len(soc) < 7:      # wildcard prefix
                    hit = [d for k, v in chains[2][0].items()
                           if k.startswith(soc) for d in v]
                    dds.update(hit)
                else:
                    got, _ = bp.lookup(soc, chains[2])
                    dds.update(got or [])
            for dd in dds:
                rows.append((dd, r.emp / max(len(dds), 1),
                             r.mem_share, r.cov_share))
    out = pd.DataFrame(rows, columns=["occ1990dd", "emp", "mem_share", "cov_share"])
    agg = (out.groupby("occ1990dd")
           .apply(lambda g: pd.Series({
               "mem_share": np.average(g["mem_share"], weights=g["emp"]),
               "cov_share": np.average(g["cov_share"], weights=g["emp"]),
               "emp_k": g["emp"].sum()}), include_groups=False)
           .reset_index())
    mapped = out["emp"].sum() / df["emp"].sum()
    note(f"unionstats {year} -> occ1990dd: {len(agg)} occupations, "
         f"{mapped:.3f} of source employment mapped")
    return agg, mapped


# ------------------------------------------------------------- licensure
def licensure_by_group():
    raw = pd.read_excel(fetch("cpsaat53.xlsx"), header=None)
    out = {}
    for i in range(len(raw)):
        name = str(raw.iloc[i, 0]).strip()
        if name in CPS_GROUP_SOC:
            share = pd.to_numeric(raw.iloc[i, 3], errors="coerce")
            if pd.notna(share):
                out[CPS_GROUP_SOC[name]] = float(share) / 100.0
    note(f"cpsaat53: licensed-or-certified shares for {len(out)} SOC major groups")
    if len(out) < 20:
        note("BLOCKED: licensure group parse incomplete.")
        raise SystemExit(1)
    return out


def dd_soc_major_weights(chains):
    """occ1990dd -> SOC-major employment weights, from the 2025 OEWS read."""
    df, _ = bp.read_oews(2025)
    rows = []
    for r in df.itertuples(index=False):
        dds, _ = None, None
        for key in ["soc18", "soc10", "soc00"]:
            dds, _ = bp.lookup(r.occ_code, dict(zip(
                ["soc00", "soc10", "soc18"], chains))[key])
            if dds:
                break
        for dd in dds or []:
            rows.append((dd, r.occ_code[:2], r.tot_emp / len(dds)))
    w = pd.DataFrame(rows, columns=["occ1990dd", "soc_major", "emp"])
    return w


def licensure_to_dd(chains):
    lic = licensure_by_group()
    w = dd_soc_major_weights(chains)
    w["lic"] = w["soc_major"].map(lic)
    w = w.dropna(subset=["lic"])
    out = (w.groupby("occ1990dd")
           .apply(lambda g: np.average(g["lic"], weights=g["emp"]),
                  include_groups=False).rename("licensed_2025").reset_index())
    note(f"licensure attached (group-level, ecological) to {len(out)} occ1990dd")
    return out


# ------------------------------------------------------------- the tests
def wavg(v, w):
    v, w = np.asarray(v, float), np.asarray(w, float)
    m = np.isfinite(v) & np.isfinite(w)
    return float(np.average(v[m], weights=w[m])) if m.any() else np.nan


def spearman(x, y):
    rx = pd.Series(x).rank()
    ry = pd.Series(y).rank()
    return float(np.corrcoef(rx, ry)[0, 1])


def run_tests(wedges):
    attrs = pd.read_csv(os.path.join(DATA, "occ1990dd_attributes.csv"))
    wedges = wedges.merge(attrs[["occ1990dd", "task_routine"]],
                          on="occ1990dd", how="left")
    t1, t2, t3 = [], [], []
    for rule in RULES:
        f = pd.read_csv(os.path.join(DATA, f"flips_{rule}.csv"))
        d = f.merge(wedges, on="occ1990dd", how="left")
        d["terc"] = pd.qcut(d["task_routine"], 3, labels=["low", "mid", "high"])
        flipped = d[d["flipped"] == True].dropna(subset=["cov_9901"])  # noqa: E712
        for lo, hi, lab in COHORTS:
            c = flipped[flipped["flip_year"].between(lo, hi)]
            t1.append({"rule": rule, "cohort": lab, "n": len(c),
                       "cov_9901": wavg(c["cov_9901"], c["emp_base"]),
                       "mem_9901": wavg(c["mem_9901"], c["emp_base"])})
        rho = spearman(flipped["flip_year"], flipped["cov_9901"])
        t1.append({"rule": rule, "cohort": "spearman_flipyear_cov", "n": len(flipped),
                   "cov_9901": rho, "mem_9901": np.nan})
        for terc in ["low", "mid", "high"]:
            ft = flipped[flipped["terc"] == terc]
            if len(ft) >= MIN_COHORT_N:
                t2.append({"rule": rule, "routine_terc": terc, "n": len(ft),
                           "spearman": spearman(ft["flip_year"], ft["cov_9901"]),
                           "cov_early": wavg(
                               ft[ft["flip_year"] <= 2007]["cov_9901"],
                               ft[ft["flip_year"] <= 2007]["emp_base"]),
                           "cov_late": wavg(
                               ft[ft["flip_year"] >= 2016]["cov_9901"],
                               ft[ft["flip_year"] >= 2016]["emp_base"])})
        surv = d[d["flipped"] != True].dropna(subset=["cov_9901"])     # noqa: E712
        t3.append({"rule": rule,
                   "flipped_cov_9901": wavg(flipped["cov_9901"], flipped["emp_base"]),
                   "surv_cov_9901": wavg(surv["cov_9901"], surv["emp_base"]),
                   "flipped_cov_2025": wavg(flipped["cov_2025"], flipped["emp_base"]),
                   "surv_cov_2025": wavg(surv["cov_2025"], surv["emp_base"]),
                   "flipped_licensed": wavg(flipped["licensed_2025"], flipped["emp_base"]),
                   "surv_licensed": wavg(surv["licensed_2025"], surv["emp_base"])})
    return pd.DataFrame(t1), pd.DataFrame(t2), pd.DataFrame(t3)


# ------------------------------------------------------------- figure
def draw(t1, t3):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    labs = [c[2] for c in COHORTS]
    width = 0.25
    colors = {"d30": "tab:blue", "d40": "tab:orange", "d50": "tab:green"}
    for k, rule in enumerate(RULES):
        rows = t1[(t1["rule"] == rule) & t1["cohort"].isin(labs)]
        vals = [100 * rows[rows["cohort"] == c]["cov_9901"].iloc[0] for c in labs]
        ns = [int(rows[rows["cohort"] == c]["n"].iloc[0]) for c in labs]
        x = np.arange(len(labs)) + (k - 1) * width
        ax1.bar(x, vals, width, color=colors[rule], label=f"rule {rule}")
        for xi, vi, ni in zip(x, vals, ns):
            ax1.text(xi, vi + 0.4, f"n={ni}", fontsize=6.5, ha="center")
    ax1.set_xticks(np.arange(len(labs)))
    ax1.set_xticklabels([f"flipped {c}" for c in labs])
    ax1.set_ylim(0, 23)                      # headroom: n-labels clear the legend
    ax1.set_ylabel("pre-period union coverage, 1999–2001 (%)")
    ax1.set_title("Targeting order: the wedge content of each flip cohort")
    ax1.legend(fontsize=8)

    cats = ["union cov. 1999–2001", "union cov. 2025", "licensed/certified 2025"]
    f_vals = [100 * t3[t3["rule"] == "d40"][c].iloc[0]
              for c in ["flipped_cov_9901", "flipped_cov_2025", "flipped_licensed"]]
    s_vals = [100 * t3[t3["rule"] == "d40"][c].iloc[0]
              for c in ["surv_cov_9901", "surv_cov_2025", "surv_licensed"]]
    x = np.arange(len(cats))
    ax2.bar(x - 0.2, f_vals, 0.4, label="flipped (rule d40)", color="tab:red", alpha=0.8)
    ax2.bar(x + 0.2, s_vals, 0.4, label="surviving", color="tab:blue")
    ax2.set_xticks(x)
    ax2.set_xticklabels(cats, fontsize=8)
    ax2.set_ylabel("share of employment (%)")
    ax2.set_title("What protection survives: price-form vs quantity-form")
    ax2.legend(fontsize=8)

    fig.tight_layout()
    fp = os.path.join(FIGS, "wedge_targeting.png")
    fig.savefig(fp, dpi=150)
    note(f"wrote figures/{os.path.basename(fp)}")


if __name__ == "__main__":
    note("=== wedge layer build (unit 4): family C + targeting-order test ===")
    chains = bp.build_chains()

    pre = []
    for y in [1999, 2000, 2001]:
        agg, mapped = union_to_dd(read_unionstats(y), y, chains)
        if mapped < 0.85:
            note(f"BLOCKED: unionstats {y} mapping below 0.85.")
            raise SystemExit(1)
        pre.append(agg.set_index("occ1990dd"))
    pre_avg = (pd.concat(pre).groupby("occ1990dd")
               .agg(cov_9901=("cov_share", "mean"), mem_9901=("mem_share", "mean"),
                    emp_k_9901=("emp_k", "mean")).reset_index())

    u25, mapped25 = union_to_dd(read_unionstats(2025), 2025, chains)
    if mapped25 < 0.80:      # extra hop through SOC2018; slightly looser floor
        note("BLOCKED: unionstats 2025 mapping below 0.80.")
        raise SystemExit(1)
    u25 = u25.rename(columns={"cov_share": "cov_2025", "mem_share": "mem_2025",
                              "emp_k": "emp_k_2025"})

    lic = licensure_to_dd(chains)
    wedges = (pre_avg.merge(u25, on="occ1990dd", how="outer")
              .merge(lic, on="occ1990dd", how="left"))
    note(f"wedge table: {len(wedges)} occ1990dd rows "
         f"({wedges['cov_9901'].notna().sum()} with pre-period coverage, "
         f"{wedges['licensed_2025'].notna().sum()} with licensure)")

    t1, t2, t3 = run_tests(wedges)
    wedges.to_csv(os.path.join(DATA, "wedges_occ1990dd.csv"), index=False)
    t1.to_csv(os.path.join(DATA, "targeting_cohorts.csv"), index=False)
    t2.to_csv(os.path.join(DATA, "targeting_by_routine.csv"), index=False)
    t3.to_csv(os.path.join(DATA, "protection_survival.csv"), index=False)
    draw(t1, t3)
    with open(os.path.join(DATA, "wedges_ledger.txt"), "w", encoding="utf8") as fh:
        fh.write("\n".join(ledger) + "\n")

    print("\n=== T1: targeting order (pre-period union coverage by flip cohort) ===")
    print(t1.round(3).to_string(index=False))
    print("\n=== T2: within routine terciles ===")
    print(t2.round(3).to_string(index=False))
    print("\n=== T3: protection of survivors vs flipped ===")
    print(t3.round(3).to_string(index=False))
    note("wrote data/wedges_occ1990dd.csv, targeting_cohorts.csv, "
         "targeting_by_routine.csv, protection_survival.csv, wedges_ledger.txt")
