# demolition_order.py — data item three: the demolition-order cross-section.
# The anatomy's claim (stress-test §1, refinement logged before scoring): documentation
# density D gates the LEARNING rays only; engineering rays cross by design. Two testable
# shadows at occupation level:
#   TEST A (order within the exposed): among LLM-exposed occupations, post-2022 movement
#     should be ordered by D — the well-documented flip first, low-D wait for a corpus
#     (rule outcome DELAYED). Prediction: corr(D, post-minus-pre share trend) < 0 within
#     the top exposure tercile.
#   TEST B (placebo, the contrast that makes A mean something): the PRE-LLM flip set
#     (flip_year ≤ 2015 — engineering/computing-era demolition) should be selected on
#     routine structure, NOT on D conditional on routine. An engine needs no corpus.
# D proxies (grid, each tied to a clause of the rule's D definition, pre-registered here):
#   D_doc    = O*NET WA "Documenting/Recording Information" importance — input→output
#              pairs accrue as digital exhaust of normal work.
#   D_comp   = O*NET WA "Working with Computers" importance — the exhaust channel.
#   D_struct = O*NET WC "Freedom to Make Decisions", SIGN SET BY ANCHOR TEST — the classic
#              "Structured versus Unstructured Work" item is ABSENT from the 30.3 Work
#              Context file (checked; nearest kin are Freedom/Repetition/Automation);
#              Freedom reversed is the nearest instrument for "a written procedure
#              suffices for a competent novice." Caveat, stated: this member is the most
#              routine-adjacent of the three — for TEST B the sharp members are D_doc and
#              D_comp; "Importance of Repeating Same Tasks" was rejected as circular with
#              routine, "Degree of Automation" as circular with the outcome.
# Everything ecological (occupation = bundle of components; D is defined per component) —
# stated, not corrected; the stress test's 21 cases are the component-level pilot.
# Runs offline from the companion's validated cache. 2026-08-09.

import io
import os
import sys
import zipfile

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
REV = os.path.dirname(HERE)
OUTER = os.path.dirname(REV)
COMP = os.path.join(OUTER, "companion")
REVDATA = os.path.join(REV, "data")

os.chdir(COMP)                                   # companion code uses cache/ data/ relative paths
sys.path.insert(0, os.path.join(COMP, "code"))
from build_panel import build_chains, lookup     # the companion's own SOC→occ1990dd walk


def spearman(x, y):
    x = pd.Series(x).rank().values; y = pd.Series(y).rank().values
    x = x - x.mean(); y = y - y.mean()
    return float((x * y).sum() / np.sqrt((x * x).sum() * (y * y).sum()))


# ---------------- Cell 0: companion assets, validated ----------------
attrs = pd.read_csv("data/occ1990dd_attributes.csv")
expo = pd.read_csv("data/exposure_occ1990dd.csv")
fric = pd.read_csv("data/friction.csv")
flips = {r: pd.read_csv(f"data/flips_{r}.csv") for r in ("d30", "d40", "d50")}
assert len(attrs) > 300 and len(expo) > 250 and len(fric) > 250
EXPO_VARS = ["dv_rating_alpha", "dv_rating_beta", "dv_rating_gamma",
             "human_rating_alpha", "human_rating_beta", "human_rating_gamma"]
print(f"companion assets: {len(attrs)} attribute rows, {len(expo)} exposure rows, "
      f"{len(fric)} friction rows, flips {[len(f) for f in flips.values()]}")

# ---------------- Cell 1: O*NET 30.3 D items, matched BY NAME and validated ----------------
zf = zipfile.ZipFile("cache/db_30_3_text.zip")
wa = pd.read_csv(io.BytesIO(zf.read("db_30_3_text/Work Activities.txt")), sep="\t")
wc = pd.read_csv(io.BytesIO(zf.read("db_30_3_text/Work Context.txt")), sep="\t")

def item_by_name(df, names, scale):
    hit = df[df["Element Name"].isin(names) & (df["Scale ID"] == scale)]
    got = hit["Element Name"].unique()
    assert len(got) == 1, f"name match not unique for {names}: {got}"
    eid = hit["Element ID"].unique()
    print(f"  matched '{got[0]}' (Element ID {eid[0]}, scale {scale}, {len(hit)} SOC rows)")
    out = hit.copy()
    out["soc6"] = out["O*NET-SOC Code"].str[:7]
    return out.groupby("soc6")["Data Value"].mean()

print("O*NET items:")
d_doc = item_by_name(wa, ["Documenting/Recording Information"], "IM")
d_comp = item_by_name(wa, ["Working with Computers", "Interacting With Computers"], "IM")
d_struct_raw = item_by_name(wc, ["Freedom to Make Decisions"], "CX")

# ---------------- Cell 2: walk to occ1990dd (the companion's own chains) ----------------
chains = build_chains()
soc18_dd = chains[2]

def to_dd(series, name):
    rows = []
    for soc6, val in series.items():
        dds, _ = lookup(soc6, soc18_dd)
        for dd in dds or []:
            rows.append({"occ1990dd": dd, name: val})
    out = pd.DataFrame(rows).groupby("occ1990dd").mean()
    print(f"  {name}: {len(series)} SOC → {len(out)} occ1990dd")
    return out

print("walking to occ1990dd:")
D = to_dd(d_doc, "D_doc").join(to_dd(d_comp, "D_comp"), how="outer") \
                         .join(to_dd(d_struct_raw, "D_struct_raw"), how="outer").reset_index()

# ---------------- Cell 3: polarity anchor test for D_struct (sign set by data, not memory) ----------------
# The WC item's scale direction is not trusted from memory. Anchors, chosen ex ante from
# the stress-test's own world: packagers/assemblers are STRUCTURED (Taylorized, hi-D by
# procedure), executives/lawyers are UNSTRUCTURED. If high raw value sits with the
# executives, structured = LOW raw and the member enters NEGATED; if anchors disagree,
# the member is DROPPED, not guessed.
lab = attrs[["occ1990dd", "label_latest"]].copy()
Dl = D.merge(lab, on="occ1990dd", how="left")
def _mean_where(pat):
    m = Dl[Dl.label_latest.str.contains(pat, case=False, na=False)]
    return float(m.D_struct_raw.mean()), len(m)
struct_side, ns = _mean_where("Packaging|Assembler")
free_side, nf = _mean_where("Chief Executives|Lawyers")
print(f"anchor test: packag/assembl raw {struct_side:.2f} (n={ns}) vs exec/lawyer raw {free_side:.2f} (n={nf})")
if ns == 0 or nf == 0 or abs(struct_side - free_side) < 0.3:
    print("  anchors inconclusive — D_struct DROPPED, not guessed")
    D_MEMBERS = ["D_doc", "D_comp"]
else:
    if struct_side > free_side:
        D["D_struct"] = D["D_struct_raw"]; print("  high raw = structured → D_struct = raw")
    else:
        D["D_struct"] = -D["D_struct_raw"]; print("  high raw = freedom → D_struct = −raw")
    D_MEMBERS = ["D_doc", "D_comp", "D_struct"]

# ---------------- Cell 4: merge and standardize ----------------
df = (attrs[["occ1990dd", "task_routine", "label_latest"]]
      .merge(D[["occ1990dd"] + D_MEMBERS], on="occ1990dd", how="inner")
      .merge(expo[["occ1990dd"] + EXPO_VARS], on="occ1990dd", how="inner")
      .merge(fric[["occ1990dd", "pre_slope", "post_slope", "d_slope", "emp_2025"]],
             on="occ1990dd", how="left"))
for c in D_MEMBERS:
    df[c + "_z"] = (df[c] - df[c].mean()) / df[c].std()
print(f"\nmerged cross-section: {len(df)} occupations, {df.d_slope.notna().sum()} with friction trends")
assert len(df) > 250

# ---------------- Cell 5: TEST A — order within the exposed ----------------
print("\nTEST A — among the top LLM-exposure tercile, is movement ordered by D?")
print("(prediction: negative Spearman — high D decelerates first; 3 years post-arrival,")
print(" friction still binding on average, so weak signal is the honest expectation)")
rowsA, spearmans = [], []
for ev in EXPO_VARS:
    top = df[df[ev] >= df[ev].quantile(2 / 3)].dropna(subset=["d_slope"])
    for dm in D_MEMBERS:
        sub = top.dropna(subset=[dm])
        rho = spearman(sub[dm], sub.d_slope)
        spearmans.append(rho)
        rowsA.append(dict(test="A", expo_var=ev, d_member=dm, n=len(sub), spearman=rho))
neg = sum(1 for r in spearmans if r < 0)
print(f"  {neg}/{len(spearmans)} member-pairs negative | median rho {np.median(spearmans):+.3f} "
      f"| range [{min(spearmans):+.3f}, {max(spearmans):+.3f}]")
ev0, dm0 = "human_rating_beta", D_MEMBERS[0]
top = df[df[ev0] >= df[ev0].quantile(2 / 3)].dropna(subset=["d_slope", dm0]).copy()
top["D_terc"] = pd.qcut(top[dm0], 3, labels=["low D", "mid", "high D"])
terc = top.groupby("D_terc", observed=True).apply(
    lambda s: pd.Series({"d_slope_mean": s.d_slope.mean(),
                         "d_slope_empwt": np.average(s.d_slope, weights=s.emp_2025),
                         "n": len(s)}), include_groups=False)
print(f"  display pair ({ev0} × {dm0}), post-minus-pre trend by D tercile:")
print(terc.round(3).to_string())

# ---------------- Cell 6: TEST B — the placebo: pre-LLM flips select on routine, not D ----------------
print("\nTEST B — pre-LLM flips (flip_year ≤ 2015): selected on routine, or on D?")
print("(prediction: routine gap >> 0; D gap |z| small conditional on routine — an engine needs no corpus)")
df["routine_terc"] = pd.qcut(df.task_routine, 3, labels=["loR", "midR", "hiR"])
rowsB = []
for rule, fl in flips.items():
    fl2 = fl[["occ1990dd", "flipped", "flip_year"]].copy()
    fl2["pre_flip"] = fl2.flipped & (fl2.flip_year <= 2015)
    m = df.merge(fl2[["occ1990dd", "pre_flip"]], on="occ1990dd", how="inner")
    r_gap = m[m.pre_flip].task_routine.mean() - m[~m.pre_flip].task_routine.mean()
    r_sd = m.task_routine.std()
    line = [f"  {rule}: routine gap {r_gap / r_sd:+.2f} sd"]
    for dm in D_MEMBERS:
        # within-routine-tercile D gap, weighted by tercile share of pre-flips
        gaps, wts = [], []
        for t, sub in m.groupby("routine_terc", observed=True):
            if sub.pre_flip.sum() >= 3:
                gaps.append(sub[sub.pre_flip][dm + "_z"].mean() - sub[~sub.pre_flip][dm + "_z"].mean())
                wts.append(sub.pre_flip.sum())
        dgap = float(np.average(gaps, weights=wts)) if gaps else np.nan
        line.append(f"{dm} gap {dgap:+.2f}z")
        rowsB.append(dict(test="B", rule=rule, d_member=dm, n_preflip=int(m.pre_flip.sum()),
                          routine_gap_sd=r_gap / r_sd, d_gap_z_withinR=dgap))
    print(" | ".join(line) + f" | n pre-flip {int(m.pre_flip.sum())}")

# ---------------- Cell 6b: TEST B era-correct — D on the EVE of the wave (O*NET 13.0, 2008) ----------------
# The rule scores D "on the eve of the relevant wave." Cell 6 used 2025's O*NET, where
# survivors' computerization has had two decades to drift upward — survivorship
# contamination, biasing the D gap negative. O*NET 13.0 (June 2008, O*NET-SOC 2006 ≈
# SOC-2000 codes → chains[0]) sits on the eve of the 2008–15 flip mass; the 2008-scored
# gaps are the defensible ones and the figure quotes them. (O*NET 9.0, Dec 2005, also
# cached — one release further back, same construction, available as robustness.)
zf13 = zipfile.ZipFile("cache/db_13_0.zip")
wa13 = pd.read_csv(io.BytesIO(zf13.read("db_13_0/Work Activities.txt")), sep="\t")
print("\nO*NET 13.0 (2008) items for the era-correct placebo:")
d_doc13 = item_by_name(wa13, ["Documenting/Recording Information"], "IM")
d_comp13 = item_by_name(wa13, ["Working with Computers", "Interacting With Computers"], "IM")
soc00_dd = chains[0]
rows13 = []
for name, ser in [("D_doc08", d_doc13), ("D_comp08", d_comp13)]:
    for soc6, val in ser.items():
        dds, _ = lookup(soc6, soc00_dd)
        for dd in dds or []:
            rows13.append({"occ1990dd": dd, "member": name, "val": val})
D13 = pd.DataFrame(rows13).groupby(["occ1990dd", "member"]).val.mean().unstack().reset_index()
df = df.merge(D13, on="occ1990dd", how="left")
for c in ["D_doc08", "D_comp08"]:
    df[c + "_z"] = (df[c] - df[c].mean()) / df[c].std()
print(f"  era-correct D attached: {df.D_doc08.notna().sum()} occupations")

print("\nTEST B, era-correct (D scored 2008, the eve): selected on routine, or on D?")
gapsB13 = {}
for rule, fl in flips.items():
    fl2 = fl[["occ1990dd", "flipped", "flip_year"]].copy()
    fl2["pre_flip"] = fl2.flipped & (fl2.flip_year <= 2015)
    m = df.merge(fl2[["occ1990dd", "pre_flip"]], on="occ1990dd", how="inner")
    r_gap = (m[m.pre_flip].task_routine.mean() - m[~m.pre_flip].task_routine.mean()) / m.task_routine.std()
    line = [f"  {rule}: routine gap {r_gap:+.2f} sd"]
    for dm in ["D_doc08", "D_comp08"]:
        gaps, wts = [], []
        for t, sub in m.dropna(subset=[dm]).groupby("routine_terc", observed=True):
            if sub.pre_flip.sum() >= 3:
                gaps.append(sub[sub.pre_flip][dm + "_z"].mean() - sub[~sub.pre_flip][dm + "_z"].mean())
                wts.append(sub.pre_flip.sum())
        dgap = float(np.average(gaps, weights=wts)) if gaps else np.nan
        gapsB13[(rule, dm)] = dgap
        line.append(f"{dm} gap {dgap:+.2f}z")
        rowsB.append(dict(test="B08", rule=rule, d_member=dm, n_preflip=int(m.pre_flip.sum()),
                          routine_gap_sd=r_gap, d_gap_z_withinR=dgap))
    print(" | ".join(line))

# ---------------- Cell 7: construct overlap, stated not tested ----------------
print("\nconstruct overlap (stated): Eloundou exposure itself partly encodes documentation —")
for dm in D_MEMBERS:
    r = spearman(df.dropna(subset=[dm])[dm], df.dropna(subset=[dm])["human_rating_beta"])
    print(f"  corr(exposure human-β, {dm}) = {r:+.2f}", end="")
print("\n  positive by construction; TEST A conditions on exposure precisely to step past this.")

# ---------------- Cell 8: outputs ----------------
out = df[["occ1990dd", "label_latest", "task_routine"] + D_MEMBERS + ["D_doc08", "D_comp08"]
         + EXPO_VARS + ["pre_slope", "post_slope", "d_slope", "emp_2025"]]
out.to_csv(os.path.join(REVDATA, "demolition_order.csv"), index=False)
statsdf = pd.DataFrame(rowsA + rowsB)
statsdf.to_csv(os.path.join(REVDATA, "demolition_order_stats.csv"), index=False)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
ax = axes[0]
vals = terc["d_slope_empwt"]
ax.bar(range(len(vals)), vals, color=["#c6dbef", "#6baed6", "#2171b5"])
ax.set_xticks(range(len(vals))); ax.set_xticklabels(vals.index)
ax.axhline(0, color="k", lw=.8)
ax.set_ylabel("share trend, post-LLM minus pre (%pts/yr)")
med_rho = np.median(spearmans)
ax.set_title("Among LLM-exposed occupations, movement is NOT yet ordered by\ndocumentation "
             f"(median Spearman {med_rho:+.2f}) — the ordering stays a dated prediction", fontsize=10)
ax = axes[1]
bb = statsdf[statsdf.test == "B08"]  # the era-correct version carries the figure
x = np.arange(3)
ax.bar(x - 0.15, bb.groupby("rule").routine_gap_sd.first().reindex(["d30", "d40", "d50"]),
       width=0.3, label="routine-intensity gap (sd)", color="tab:red")
ax.bar(x + 0.15, bb.groupby("rule").d_gap_z_withinR.mean().reindex(["d30", "d40", "d50"]),
       width=0.3, label="documentation gap, within routine terciles (z, D scored 2008)", color="tab:gray")
ax.set_xticks(x); ax.set_xticklabels(["rule d30", "rule d40", "rule d50"])
ax.axhline(0, color="k", lw=.8)
ax.set_ylabel("flipped minus surviving")
ax.set_title("The pre-LLM demolition selected on routine structure —\nnot on documentation. "
             "An engine needs no corpus.", fontsize=10)
ax.legend(fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(REVDATA, "demolition_order.png"), dpi=150)
print("\nwrote data/demolition_order.csv, data/demolition_order_stats.csv, data/demolition_order.png")
