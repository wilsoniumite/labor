# build_righttail.py — unit 3: family B, the right tail (spec:
# companion_schedule_spec.md). Family A's envelope is censored at the
# waterline; this unit reads the censored segment with capability sources
# over the years the premise is live:
#
#   Exposure layer (Eloundou et al., MIT license): occupation-resolved LLM
#   exposure, six published variants (rater {gpt4 dv, human} x aggregation
#   {alpha, beta, gamma}) — the variants ARE the mapping grid; no mapping of
#   our own is invented. Mapped soc8 -> soc6 -> occ1990dd via the unit-1
#   chains (mean across mapped codes, the unit-1 O*NET convention).
#
#   The clock (Epoch benchmark hub, CC-BY): dated frontier traces — the
#   Epoch Capabilities Index, GPQA Diamond, SWE-bench Verified, and the
#   republished METR time-horizon series (the human-anchored member:
#   human_minutes defines the scale, so no external human-baseline constant
#   is injected anywhere). Doubling time fit on the dated horizon series.
#
#   Validation member: METR raw runs.jsonl (research data published for the
#   METR time-horizon paper; the repo README points to a LICENSE file that
#   is ABSENT from the repository — recorded in README/data note; Epoch's
#   CC-BY republication is the licensing-clean copy this build treats as
#   primary). Per-model 50% horizons are recomputed from raw runs by
#   weighted logistic regression on log2(human_minutes) and validated
#   against Epoch's published values on name-matched models.
#
# Pre-registered honesty (spec): benchmarks oversample verifiable tasks —
# stated, not corrected. Exposure is an LLM-era measure; family A's early
# flips were software/robotics-era. The join below reports the surviving
# (unflipped) mass by exposure — the premise's live segment — without
# claiming exposure explains historical flips.
import io
import json
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
import build_panel as bp  # noqa: E402  (chains + lookup, cache-served)

EXP_VARIANTS = ["dv_rating_alpha", "dv_rating_beta", "dv_rating_gamma",
                "human_rating_alpha", "human_rating_beta", "human_rating_gamma"]
RULES = ["d30", "d40", "d50"]
DOUBLING_BAND_MONTHS = (4.0, 12.0)   # sanity vs METR's published ~7 months
# raw-vs-published matching is RULE-BASED ONLY (exact, then unique prefix,
# preferring Epoch's METR-tagged rows; ambiguous variants dropped, never
# guessed) — naming conventions diverge (inspect-suffixed ids vs API-dated
# names, order flips like claude_4_opus vs claude-opus-4), so the floor is
# sized to what is matchable without judgment calls
MIN_MATCHED = 10
MIN_EXP_ROWS = 300

ledger = []


def note(msg):
    ledger.append(msg)
    print(msg)


# ---------------------------------------------------------------- exposure
def build_exposure(chains):
    occ = pd.read_csv(fetch("eloundou_occ_level.csv"))
    occ["soc6"] = occ["O*NET-SOC Code"].str[:7]
    per_soc = occ.groupby("soc6")[EXP_VARIANTS].mean().reset_index()
    rows = []
    for r in per_soc.itertuples(index=False):
        dds, _ = bp.lookup(r.soc6, chains[2])
        for dd in dds or []:
            rows.append({"occ1990dd": dd,
                         **{v: getattr(r, v) for v in EXP_VARIANTS}})
    exp = (pd.DataFrame(rows).groupby("occ1990dd")
           .agg(**{v: (v, "mean") for v in EXP_VARIANTS},
                n_soc_sources=(EXP_VARIANTS[0], "size")).reset_index())
    note(f"exposure: {len(per_soc)} soc6 -> {len(exp)} occ1990dd rows "
         f"(variants = Eloundou's published six; mean across mapped codes)")
    if len(exp) < MIN_EXP_ROWS:
        note(f"BLOCKED: exposure rows {len(exp)} < {MIN_EXP_ROWS}.")
        raise SystemExit(1)
    return exp


def build_right_tail(exp):
    panel = pd.read_csv(os.path.join(DATA, "oews_occ1990dd_panel.csv"))
    p25 = (panel[panel["year"] == 2025]
           [["occ1990dd", "emp", "top_source_title"]]
           .rename(columns={"emp": "emp_2025"}))
    out = p25.merge(exp, on="occ1990dd", how="left")
    for rule in RULES:
        f = pd.read_csv(os.path.join(DATA, f"flips_{rule}.csv"))
        out = out.merge(f[["occ1990dd", "flipped", "flip_year"]]
                        .rename(columns={"flipped": f"flipped_{rule}",
                                         "flip_year": f"flip_year_{rule}"}),
                        on="occ1990dd", how="left")
    cov = out.dropna(subset=[EXP_VARIANTS[0]])["emp_2025"].sum() / out["emp_2025"].sum()
    note(f"right tail: exposure covers {cov:.3f} of 2025 employment")
    if cov < 0.85:
        note("BLOCKED: exposure coverage below 0.85.")
        raise SystemExit(1)

    stats = []
    for rule in RULES:
        alive = out[out[f"flipped_{rule}"] != True]          # noqa: E712
        dead = out[out[f"flipped_{rule}"] == True]           # noqa: E712
        for v in EXP_VARIANTS:
            a = alive.dropna(subset=[v])
            top = a[a[v] >= 0.5]
            stats.append({
                "rule": rule, "variant": v,
                "surv_emp_wmean": np.average(a[v], weights=a["emp_2025"]),
                "surv_share_ge50": top["emp_2025"].sum() / a["emp_2025"].sum(),
                "dead_emp_wmean": (np.average(dead.dropna(subset=[v])[v],
                                              weights=dead.dropna(subset=[v])["emp_2025"])
                                   if len(dead.dropna(subset=[v])) else np.nan)})
    stats = pd.DataFrame(stats)
    med = stats[stats["rule"] == "d40"]["surv_share_ge50"].median()
    note(f"headline (d40, median variant): {med:.3f} of surviving 2025 "
         f"employment sits at exposure >= 0.5")
    return out, stats


# ---------------------------------------------------------------- the clock
def _epoch_csv(member):
    zb = zipfile.ZipFile(fetch("epoch_benchmark_data.zip"))
    df = pd.read_csv(io.BytesIO(zb.read(member)))
    df["date"] = pd.to_datetime(df["Release date"], errors="coerce")
    return df.dropna(subset=["date"])


def build_clock():
    traces = []
    for member, name, col in [
            ("epoch_capabilities_index.csv", "eci", "ECI Score"),
            ("gpqa_diamond.csv", "gpqa_diamond", "mean_score"),
            ("swe_bench_verified.csv", "swe_bench_verified", "mean_score"),
            ("metr_time_horizons_external.csv", "metr_horizon_min", "Time horizon")]:
        df = _epoch_csv(member)
        d = (df[["date", "Model version", col]]
             .rename(columns={col: "value", "Model version": "model"}))
        d["source"] = name
        # deterministic order: date ties broken by model name (sort_values on
        # date alone is an unstable quicksort — cummax would depend on it)
        d = d.dropna(subset=["value"]).sort_values(["date", "model", "value"])
        d["frontier"] = d["value"].cummax()
        traces.append(d)
        note(f"clock trace {name}: {len(d)} dated points, "
             f"{d['date'].min().date()} .. {d['date'].max().date()}, "
             f"frontier {d['value'].iloc[0]:.2f} -> {d['frontier'].iloc[-1]:.2f}")
    clock = pd.concat(traces, ignore_index=True)

    h = clock[(clock["source"] == "metr_horizon_min") & (clock["value"] > 0)]
    yrs = (h["date"] - h["date"].min()).dt.days / 365.25
    slope = np.polyfit(yrs, np.log2(h["value"]), 1)[0]   # doublings per year
    dbl_months = 12.0 / slope
    lo, hi = DOUBLING_BAND_MONTHS
    note(f"METR horizon doubling time: {dbl_months:.1f} months "
         f"(fit on {len(h)} models, {h['date'].min().date()}..{h['date'].max().date()})")
    if not (lo <= dbl_months <= hi):
        note(f"BLOCKED: doubling time outside [{lo},{hi}] months — wrong pull?")
        raise SystemExit(1)
    return clock, dbl_months


def _norm_name(s):
    s = re.sub(r"\(.*?\)", "", str(s).lower())
    return re.sub(r"[^a-z0-9]", "", s)


def validate_metr_raw(clock):
    """Recompute per-model 50% horizons from raw runs; compare to Epoch's
    republished values on name-matched models (log-space correlation)."""
    recs = []
    with open(fetch("metr_runs_1_1.jsonl"), encoding="utf8") as fh:
        for line in fh:
            r = json.loads(line)
            if r.get("human_minutes") and r.get("score_binarized") is not None:
                recs.append((r.get("alias") or r.get("model"),
                             r.get("model") or "",
                             float(r["human_minutes"]),
                             int(r["score_binarized"]),
                             float(r.get("invsqrt_task_weight") or 1.0)))
    runs = pd.DataFrame(recs, columns=["alias", "model_id", "human_minutes",
                                       "success", "w"])
    note(f"metr raw: {len(runs):,} runs, {runs['alias'].nunique()} models")

    def horizon50(g):
        if g["success"].nunique() < 2 or len(g) < 50:
            return np.nan
        x = np.log2(g["human_minutes"].to_numpy(float))
        y = g["success"].to_numpy(float)
        w = g["w"].to_numpy(float)
        b0, b1 = 0.0, 0.0                      # weighted logistic, Newton steps
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.zeros(2)
        for _ in range(60):
            p = 1 / (1 + np.exp(-X @ beta))
            gvec = X.T @ (w * (y - p))
            H = (X * (w * p * (1 - p))[:, None]).T @ X
            try:
                step = np.linalg.solve(H + 1e-9 * np.eye(2), gvec)
            except np.linalg.LinAlgError:
                return np.nan
            beta = beta + step
            if np.max(np.abs(step)) < 1e-10:
                break
        if beta[1] >= 0:                        # success must fall with length
            return np.nan
        return float(2 ** (-beta[0] / beta[1]))

    ids = runs[["alias", "model_id"]].drop_duplicates("alias")
    mine = (runs.groupby("alias").apply(horizon50, include_groups=False)
            .dropna().rename("h50_raw").reset_index().merge(ids, on="alias"))
    ep = _epoch_csv("metr_time_horizons_external.csv").copy()
    ep["k"] = ep["Model version"].map(_norm_name)
    ep["tagged"] = ep["METR version"].notna()

    def find(row):
        for key in [_norm_name(row.model_id).replace("inspect", ""),
                    _norm_name(row.alias)]:
            if not key:
                continue
            exact = ep[ep["k"] == key]
            if len(exact):
                t = exact[exact["tagged"]]
                return (t if len(t) else exact).iloc[0]
            if len(key) >= 5:
                pref = ep[ep["k"].str.startswith(key)]
                if len(pref) == 1:
                    return pref.iloc[0]
                t = pref[pref["tagged"]]
                if len(t) == 1:
                    return t.iloc[0]
        return None

    rows = []
    for r in mine.itertuples(index=False):
        hit = find(r)
        if hit is not None:
            rows.append({"alias": r.alias, "h50_raw": r.h50_raw,
                         "epoch_model": hit["Model version"],
                         "h50_epoch": float(hit["Time horizon"])})
    m = pd.DataFrame(rows)
    m = m[(m["h50_raw"] > 0) & (m["h50_epoch"] > 0)]
    corr = np.corrcoef(np.log(m["h50_raw"]), np.log(m["h50_epoch"]))[0, 1] \
        if len(m) >= 3 else np.nan
    note(f"metr raw-vs-published: {len(m)} models matched, "
         f"log-space correlation {corr:.3f}")
    if len(m) < MIN_MATCHED or not (corr >= 0.8):
        note(f"BLOCKED: raw validation failed (need >= {MIN_MATCHED} matches, "
             f"corr >= 0.8).")
        raise SystemExit(1)
    return m


# ---------------------------------------------------------------- figure
def draw(clock, dbl_months, tail, stats):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    h = clock[(clock["source"] == "metr_horizon_min") & (clock["value"] > 0)]
    ax1.scatter(h["date"], h["value"], s=14, alpha=0.6, label="models (METR horizon)")
    yrs = (h["date"] - h["date"].min()).dt.days / 365.25
    b1, b0 = np.polyfit(yrs, np.log2(h["value"]), 1)
    xs = pd.date_range(h["date"].min(), h["date"].max(), periods=50)
    ys = 2 ** (b0 + b1 * (xs - h["date"].min()).days / 365.25)
    ax1.plot(xs, ys, "k--", lw=1.2,
             label=f"fit: doubling every {dbl_months:.1f} months")
    ax1.set_yscale("log")
    ax1.set_ylabel("50%-success task length (human minutes, log)")
    ax1.set_title("The clock: how long a task machines can hold")
    ax1.legend(loc="upper left", fontsize=8)
    for y, lab in [(60, "1 hour"), (480, "1 workday")]:
        ax1.axhline(y, color="gray", lw=0.7, ls=":")
        ax1.text(h["date"].max(), y * 1.15, lab, fontsize=7, color="gray",
                 ha="right")

    v = "human_rating_beta"                      # display variant; band in CSV
    t = tail.dropna(subset=[v]).copy()
    bins = np.arange(0, 1.1, 0.1)
    t["bin"] = pd.cut(t[v], bins, include_lowest=True)
    alive = (t[t["flipped_d40"] != True]         # noqa: E712
             .groupby("bin", observed=False)["emp_2025"].sum() / 1e6)
    dead = (t[t["flipped_d40"] == True]          # noqa: E712
            .groupby("bin", observed=False)["emp_2025"].sum() / 1e6)
    x = np.arange(len(alive))
    ax2.bar(x, alive.values, 0.8, label="surviving 2025 employment", color="tab:blue")
    ax2.bar(x, dead.values, 0.8, bottom=alive.values,
            label="already flipped (rule d40)", color="tab:red", alpha=0.75)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{max(b.left, 0):.1f}–{b.right:.1f}"
                         for b in alive.index], rotation=45, fontsize=7)
    ax2.set_xlabel("LLM exposure (Eloundou human-β variant; band across six in CSV)")
    ax2.set_ylabel("2025 employment (millions)")
    ax2.set_title("The tail under the rising water")
    ax2.legend(loc="upper right", fontsize=8)

    fig.tight_layout()
    fp = os.path.join(FIGS, "right_tail.png")
    fig.savefig(fp, dpi=150)
    note(f"wrote figures/{os.path.basename(fp)}")


if __name__ == "__main__":
    note("=== right tail build (unit 3): exposure layer + capability clock ===")
    chains = bp.build_chains()
    exp = build_exposure(chains)
    tail, stats = build_right_tail(exp)
    clock, dbl_months = build_clock()
    matched = validate_metr_raw(clock)

    exp.to_csv(os.path.join(DATA, "exposure_occ1990dd.csv"), index=False)
    tail.to_csv(os.path.join(DATA, "right_tail.csv"), index=False)
    stats.to_csv(os.path.join(DATA, "right_tail_stats.csv"), index=False)
    clock.to_csv(os.path.join(DATA, "capability_clock.csv"), index=False)
    matched.to_csv(os.path.join(DATA, "metr_raw_validation.csv"), index=False)
    draw(clock, dbl_months, tail, stats)
    with open(os.path.join(DATA, "righttail_ledger.txt"), "w", encoding="utf8") as fh:
        fh.write("\n".join(ledger) + "\n")
    print("\n=== survivor exposure stats (band across rules x variants) ===")
    print(stats.round(3).to_string(index=False))
    note("wrote data/exposure_occ1990dd.csv, right_tail.csv, right_tail_stats.csv, "
         "capability_clock.csv, metr_raw_validation.csv, righttail_ledger.txt")
