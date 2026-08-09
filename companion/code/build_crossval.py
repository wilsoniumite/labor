# build_crossval.py — unit 5: cross-validation + the reinstatement series
# (spec: companion_schedule_spec.md, the last data unit).
#
# HALF 1 — REINSTATEMENT, MEASURED. The Link closes the new-task margin by
# assumption (§9, branch two); this half measures that margin on the record
# O*NET actually keeps. Task universes are read from 23 archived database
# releases (annual majors 5.1-2003 through 30.0, plus current 30.3; release
# dates parsed live from db_releases.html, not remembered). For each
# adjacent release pair, task births and deaths are counted TWO WAYS:
#   by Task ID   — stable identifiers; misses reworded statements, so it is
#                  the churn UNDERCOUNT member;
#   by text      — normalized statement text; counts every rewording as a
#                  death+birth, so it is the churn OVERCOUNT member.
# The truth is bracketed between the members. Counts run only over
# occupations present in BOTH releases of a pair (taxonomy adds/drops are
# reported separately, not mixed into task churn), and rates are per 1,000
# base tasks per year between release dates. O*NET's own update cycle
# (occupations resurveyed in waves) makes single pairs lumpy — stated; the
# object is the trend across two decades, not any one pair.
#
# HALF 2 — THE FRICTION GAP (A x B). The clock dates LLM capability arrival
# (unit 3); this half measures the adoption RESPONSE at the occupation
# level: employment-share trend 2015-2019 (pre) vs 2022-2025 (post; 2020-21
# excluded as the covid break), the change in slope joined against LLM
# exposure. F is characterized by the open gap, not point-identified — the
# punctuated-adoption remark predicts exactly a flat phase before a jump.
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
from fetch import fetch, ONET_OLD, ONET_TXT  # noqa: E402

RELEASES = ONET_OLD + ONET_TXT + ["30_3"]
PRE_WIN = (2015, 2019)
POST_WIN = (2022, 2025)
MIN_EMP = 10_000
EXP_PRIMARY = "human_rating_beta"

ledger = []


def note(msg):
    ledger.append(msg)
    print(msg)


# ------------------------------------------------------- release dates
def release_dates():
    html = open(fetch("onet_releases_page.html"), encoding="utf8").read()
    pairs = re.findall(
        r"O\*NET (\d+\.\d+)\s*\n<span class=\"badge bg-secondary\">([A-Za-z]+ \d{4})</span>",
        html)
    out = {}
    for v, d in pairs:
        out.setdefault(v.replace(".", "_"), pd.to_datetime(d, format="%B %Y"))
    note(f"release dates parsed for {len(out)} versions (live page)")
    return out


# ------------------------------------------------------- task universes
def _norm_text(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def task_universe(ver):
    """-> DataFrame [soc, task_id (nullable), text_norm], distinct tasks."""
    name = "db_30_3_text.zip" if ver == "30_3" else f"onet_{ver}.zip"
    zf = zipfile.ZipFile(fetch(name))
    member = None
    for cand in ["task statements.txt", "tasks.txt"]:
        # EXACT basename match — endswith would also catch supplemental
        # files like "Green Task Statements.txt" (the 16.0/23.0/24.0 trap)
        hits = [n for n in zf.namelist()
                if os.path.basename(n).lower() == cand]
        if hits:
            member = hits[0]
            break
    if member is None:
        note(f"onet {ver}: NO task file found — release skipped")
        return None
    raw = zf.read(member)
    try:                       # early releases are cp1252, not utf-8
        txt = raw.decode("utf8")
    except UnicodeDecodeError:
        txt = raw.decode("cp1252")
    df = pd.read_csv(io.StringIO(txt), sep="\t", dtype=str,
                     on_bad_lines="skip", low_memory=False)
    cols = {re.sub(r"[^a-z]", "", c.lower()): c for c in df.columns}
    soc_c = cols.get("onetsoccode")
    task_c = cols.get("task")
    id_c = cols.get("taskid")
    if soc_c is None or task_c is None:
        note(f"onet {ver}: task file lacks soc/task columns — skipped")
        return None
    out = pd.DataFrame({
        "soc": df[soc_c].astype(str).str.strip(),
        "task_id": df[id_c].astype(str).str.strip() if id_c else None,
        "text_norm": df[task_c].map(_norm_text)})
    out = out[out["soc"].str.match(r"\d{2}-\d{4}\.\d{2}")]
    out = out[out["text_norm"].str.len() > 5].drop_duplicates(
        subset=["soc", "text_norm"])
    return out


def build_reinstatement():
    dates = release_dates()
    universes = {}
    for ver in RELEASES:
        u = task_universe(ver)
        if u is not None and len(u) > 1000 and ver.replace("_", ".") is not None:
            key_date = dates.get(ver)
            if key_date is None:
                note(f"onet {ver}: no release date on the page — skipped")
                continue
            universes[ver] = (key_date, u)
            note(f"onet {ver} ({key_date.date()}): {len(u):,} tasks, "
                 f"{u['soc'].nunique()} occupations, "
                 f"ids {'yes' if u['task_id'].notna().all() else 'NO'}")
    vers = sorted(universes, key=lambda v: universes[v][0])
    rows = []
    for v0, v1 in zip(vers, vers[1:]):
        d0, u0 = universes[v0]
        d1, u1 = universes[v1]
        years = (d1 - d0).days / 365.25
        socs = set(u0["soc"]) & set(u1["soc"])
        a = u0[u0["soc"].isin(socs)]
        b = u1[u1["soc"].isin(socs)]
        base = len(a)
        t0, t1 = set(zip(a["soc"], a["text_norm"])), set(zip(b["soc"], b["text_norm"]))
        births_txt, deaths_txt = len(t1 - t0), len(t0 - t1)
        if a["task_id"].notna().all() and b["task_id"].notna().all():
            i0, i1 = set(zip(a["soc"], a["task_id"])), set(zip(b["soc"], b["task_id"]))
            births_id, deaths_id = len(i1 - i0), len(i0 - i1)
        else:
            births_id = deaths_id = np.nan
        rows.append({
            "from": v0.replace("_", "."), "to": v1.replace("_", "."),
            "date0": d0.date(), "date1": d1.date(), "years": years,
            "matched_occs": len(socs), "base_tasks": base,
            "occs_added": u1["soc"].nunique() - len(socs),
            "occs_dropped": u0["soc"].nunique() - len(socs),
            "birth_rate_txt": 1000 * births_txt / base / years,
            "death_rate_txt": 1000 * deaths_txt / base / years,
            "birth_rate_id": 1000 * births_id / base / years,
            "death_rate_id": 1000 * deaths_id / base / years})
    series = pd.DataFrame(rows)
    note(f"reinstatement series: {len(series)} release pairs, "
         f"{series['date0'].iloc[0]} .. {series['date1'].iloc[-1]}")
    if len(series) < 18:
        note("BLOCKED: too few release pairs parsed.")
        raise SystemExit(1)
    # trend statistic: birth-rate slope per decade, both members. PRIMARY on
    # the mature era (2012-07 onward): the early levels partly reflect the
    # DOT->O*NET database-construction ramp, not economic task birth — the
    # full series is shown, the caveat stated, the trend read where the
    # instrument was stable.
    for m in ["birth_rate_txt", "birth_rate_id"]:
        for label, sub in [("full", series),
                           ("mature 2012+", series[pd.to_datetime(
                               series["date0"]) >= "2012-07-01"])]:
            s = sub.dropna(subset=[m])
            x = pd.to_datetime(s["date1"]).map(pd.Timestamp.toordinal) / 365.25
            sl = np.polyfit(x, s[m], 1)[0] * 10
            note(f"trend {m} ({label}): {sl:+.1f} per-1000/yr per decade "
                 f"(mean {s[m].mean():.1f}, last {s[m].iloc[-1]:.1f})")
    return series


# ------------------------------------------------------- friction half
def build_friction():
    panel = pd.read_csv(os.path.join(DATA, "oews_occ1990dd_panel.csv"))
    tail = pd.read_csv(os.path.join(DATA, "right_tail.csv"))
    emp = panel.pivot(index="year", columns="occ1990dd", values="emp")
    share = emp.div(emp.sum(axis=1), axis=0)

    def win_slope(s, lo, hi):
        w = s.loc[lo:hi].dropna()
        if len(w) < (hi - lo) or (w <= 0).any():
            return np.nan
        return np.polyfit(w.index, np.log(w), 1)[0]

    rows = []
    for j in share.columns:
        if emp[j].mean() < MIN_EMP:
            continue
        pre = win_slope(share[j], *PRE_WIN)
        post = win_slope(share[j], *POST_WIN)
        if np.isfinite(pre) and np.isfinite(post):
            rows.append({"occ1990dd": j, "pre_slope": pre, "post_slope": post,
                         "d_slope": post - pre,
                         "emp_2025": float(emp[j].loc[2025])})
    fr = pd.DataFrame(rows).merge(
        tail[["occ1990dd", "top_source_title"] +
             [c for c in tail.columns if "rating" in c]],
        on="occ1990dd", how="left")
    note(f"friction: slopes for {len(fr)} occupations "
         f"(pre {PRE_WIN}, post {POST_WIN}, covid years excluded)")

    stats = []
    for v in [c for c in fr.columns if "rating" in c]:
        d = fr.dropna(subset=[v]).copy()
        d["terc"] = pd.qcut(d[v], 3, labels=["low", "mid", "high"])
        for t in ["low", "mid", "high"]:
            g = d[d["terc"] == t]
            stats.append({"variant": v, "exposure_terc": t, "n": len(g),
                          "d_slope_wmean": np.average(g["d_slope"],
                                                      weights=g["emp_2025"]),
                          "pre_wmean": np.average(g["pre_slope"],
                                                  weights=g["emp_2025"]),
                          "post_wmean": np.average(g["post_slope"],
                                                   weights=g["emp_2025"])})
    stats = pd.DataFrame(stats)

    # named instances: mechanical selection (top exposure among big
    # occupations) plus labeled canonical adds found by title match
    big = fr[fr["emp_2025"] >= 200_000].nlargest(8, EXP_PRIMARY)
    adds = fr[fr["top_source_title"].str.contains(
        "Interpreters|Data Entry|Telephone Operators", case=False, na=False)]
    named = (pd.concat([big, adds]).drop_duplicates("occ1990dd")
             [["occ1990dd", "top_source_title", EXP_PRIMARY,
               "pre_slope", "post_slope", "d_slope", "emp_2025"]])
    return fr, stats, named


# ------------------------------------------------------- figure
def draw(series, stats):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    x = pd.to_datetime(series["date1"])
    ax1.plot(x, series["birth_rate_txt"], "-o", ms=3, color="tab:blue",
             label="task births (text member: reword-inclusive)")
    ax1.plot(x, series["birth_rate_id"], ":o", ms=3, color="tab:blue",
             alpha=0.7, label="task births (ID member)")
    ax1.plot(x, series["death_rate_txt"], "-s", ms=3, color="tab:red",
             label="task deaths (text member)")
    ax1.plot(x, series["death_rate_id"], ":s", ms=3, color="tab:red",
             alpha=0.7, label="task deaths (ID member)")
    ax1.set_ylabel("per 1,000 base tasks, per year")
    ax1.set_title("The new-task margin, measured (O*NET releases)")
    ax1.legend(fontsize=7.5)

    d = stats[stats["variant"] == EXP_PRIMARY]
    x2 = np.arange(3)
    vals = [100 * d[d["exposure_terc"] == t]["d_slope_wmean"].iloc[0]
            for t in ["low", "mid", "high"]]
    ns = [int(d[d["exposure_terc"] == t]["n"].iloc[0])
          for t in ["low", "mid", "high"]]
    colors = ["tab:gray", "tab:blue", "tab:orange"]
    ax2.bar(x2, vals, 0.6, color=colors)
    pad = 0.04 * (max(vals) - min(vals) + 0.1)
    for xi, vi, ni in zip(x2, vals, ns):
        if vi >= 0:
            ax2.text(xi, vi + pad, f"n={ni}", fontsize=7.5, ha="center",
                     va="bottom")
        else:
            ax2.text(xi, vi - pad, f"n={ni}", fontsize=7.5, ha="center",
                     va="top")
    lo = min(vals + [0])
    ax2.set_ylim(lo - 6 * pad, max(vals + [0]) + 6 * pad)
    ax2.axhline(0, color="k", lw=0.8)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(["low exposure", "mid", "high exposure"])
    ax2.set_ylabel("Δ share trend, post-LLM minus pre (% pts of log-slope)")
    ax2.set_title("Adoption response so far: share trends before vs after the\n"
                  "LLM capability arrival (2022-25 vs 2015-19)")

    fig.tight_layout()
    fp = os.path.join(FIGS, "crossval.png")
    fig.savefig(fp, dpi=150)
    note(f"wrote figures/{os.path.basename(fp)}")


if __name__ == "__main__":
    note("=== cross-validation build (unit 5): reinstatement + friction ===")
    series = build_reinstatement()
    fr, stats, named = build_friction()

    series.to_csv(os.path.join(DATA, "reinstatement_series.csv"), index=False)
    fr.to_csv(os.path.join(DATA, "friction.csv"), index=False)
    stats.to_csv(os.path.join(DATA, "friction_stats.csv"), index=False)
    named.to_csv(os.path.join(DATA, "friction_named.csv"), index=False)
    draw(series, stats)
    with open(os.path.join(DATA, "crossval_ledger.txt"), "w", encoding="utf8") as fh:
        fh.write("\n".join(ledger) + "\n")

    print("\n=== reinstatement series ===")
    print(series.round(2).to_string(index=False))
    print("\n=== friction by exposure tercile ===")
    print(stats.round(4).to_string(index=False))
    print("\n=== named instances ===")
    print(named.round(4).to_string(index=False))
    note("wrote data/reinstatement_series.csv, friction.csv, friction_stats.csv, "
         "friction_named.csv, crossval_ledger.txt")
