# check_splits.py — the splits tracker (code/splits.py, SPLITS.md): its plumbing, its statistic, its blinding, its
# reproduction of the panel's 2,047-cut benchmark, its freeze logic, its yearly look and its results schema.
# Mechanical checks: they test the machinery, not the readings, so they stay green as new data arrive.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_splits.py   (after code/splits.py)
# Exit status 0 only if every check passes.

from __future__ import annotations

import contextlib
import copy
import datetime as dt
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import splits as S  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


J = json.load(open(S.RESULTS, encoding="utf-8"))


def cached(sid, folder=S.CACHE):
    return S._parse(open(os.path.join(folder, sid + ".csv")).read(), sid)


ALL = {sid: cached(sid) for sid in S.MANIFEST}

# ---------------------------------------------------------------------------------------------------------------------
# S1 the series resolve. Before the freeze FRED's title must be the manifest's; after it, a title FRED has since
# changed is reported against the title recorded in the baseline (a rename is not a code fix).
titles = json.load(open(os.path.join(S.CACHE, "titles.json"), encoding="utf-8"))
bl_titles = {sid: v.get("fred_title") for sid, v in ((J["status"].get("frozen") and S.freeze_state()[1] or {}).get("series") or {}).items()}
bad, renamed = [], []
for sid, (title, _src) in S.MANIFEST.items():
    fp = os.path.join(S.CACHE, sid + ".csv")
    n = len(cached(sid)) if os.path.exists(fp) else 0
    t = titles.get(sid, {})
    if n < 10 or t.get("status") != 200:
        bad.append((sid, n, t.get("status")))
    elif t.get("title") != title:
        if bl_titles.get(sid) and t.get("title") != bl_titles[sid]:
            renamed.append((sid, bl_titles[sid], t.get("title")))
        elif not bl_titles:
            bad.append((sid, "title", t.get("title")))
check("S1 every manifest series is cached with data and its FRED page answers; before the freeze FRED's own title is the "
      "manifest's title (each ID is the concept the protocol names); after it a renamed series is reported, not failed",
      not bad and len(S.MANIFEST) == len(titles),
      f"{len(S.MANIFEST)} series; problems {bad}" + (f"; renamed since the freeze {renamed}" if renamed else ""))

# S2 blinding
refuse = ["LRHUTTTTSEM156S", "LRUN64TTSEQ156S", "LFWA64TTSEQ647S", "LREM64TTDEM156S", "SLUEM1524ZSSWE", "une_rt_a", "lfsa_argan",
          "AM0401", "AKU_unemployment.csv", "EMP_TEMP_SEX_ECO_INS_NB_A_SWE_all.csv",
          os.path.join(ROOT, "cache", "scb", "lfs_unemp_q_sa.json"), os.path.join(ROOT, "cache", "ilo", "toc.csv"), "LRHUTTTTEZM156S"]
refused = []
for x in refuse:
    try:
        S.guard(x)
    except PermissionError:
        refused.append(x)
passes = []
for sid in list(S.MANIFEST) + list(S.SCB_FILES):
    try:
        S.guard(sid)
        passes.append(sid)
    except PermissionError:
        pass
EUROPE = r"(?i)\b(sweden|swedish|euro|europe|german|france|italy|spain|netherlands|united kingdom|denmark|finland|norway)"
named = [sid for sid, (t, _) in S.MANIFEST.items() if re.search(EUROPE, t) or re.search(EUROPE, titles.get(sid, {}).get("title") or "")]
src = open(os.path.join(ROOT, "code", "splits.py"), encoding="utf-8").read()
hosts = set(re.findall(r"https?://([a-z0-9.\-]+)", src))
meta = {fn: json.load(open(os.path.join(S.SCB, fn), encoding="utf-8"))["metadata"][0]["infofile"] for fn in S.SCB_FILES}
check("S2 blinding: the guard refuses European labour-force identifiers and files (OECD rates, Eurostat, ILO, Statistics "
      "Sweden AKU/LFS) and passes every manifest entry; no manifest series names a European country; the code fetches only "
      "from FRED; the Swedish watch item reads sector accounts (NR0103) only",
      len(refused) == len(refuse) and len(passes) == len(S.MANIFEST) + len(S.SCB_FILES) and not named
      and hosts <= {"fred.stlouisfed.org"} and set(meta.values()) == {"NR0103"},
      f"refused {len(refused)}/{len(refuse)}; manifest passes {len(passes)}/{len(S.MANIFEST) + len(S.SCB_FILES)}; "
      f"European names {named}; hosts {sorted(hosts)}; SCB tables {meta}")

# S3 the statistic, on synthetic series with a known excess
idx = pd.date_range("1985-01-01", "2026-09-01", freq="MS")
t_ = np.arange(len(idx))
gap = pd.Series(0.10 * t_ + 0.5 * np.sin(2 * np.pi * t_ / 37) + 0.3 * np.cos(2 * np.pi * t_ / 11), idx)
rec = {m for m in pd.date_range("2001-04-01", "2001-11-01", freq="MS")} | {m for m in pd.date_range("2008-01-01", "2009-06-01", freq="MS")}
gap_r = gap.copy()
troughs = {pd.Timestamp("2001-11-01"), pd.Timestamp("2009-06-01")}
for m in rec - troughs:            # wild values inside recessions must not reach the reference (the trough month's level
    gap_r[m] += 50 * np.sin(m.month)  # is the next normal window's starting point, so it may)
ch = gap - gap.shift(12)
ref = S.reference(ch, "MS", 12, rec, 120)
ref_r = S.reference(gap_r - gap_r.shift(12), "MS", 12, rec, 120)
manual = ch[[t for t in ch.dropna().index if "1990-01-01" <= str(t.date()) <= "2019-12-31"
             and not any(m in rec for m in pd.date_range(t - pd.DateOffset(months=11), t, freq="MS"))]]
target = 2.5
g2 = gap.copy()
g2.iloc[-1] = g2.iloc[-13] + ref["mean"] + target * ref["sd"]
E_up = float(S.e_series(g2 - g2.shift(12), ref, +1).iloc[-1])
E_dn = float(S.e_series(g2 - g2.shift(12), ref, -1).iloc[-1])
short_ch = ch[ch.index >= "2020-06-01"]
short = S.reference(short_ch, "MS", 12, rec, 120, upto=short_ch.index[-1] - pd.DateOffset(months=12))
sp6 = S.SPEC["output_per_hour"]
qidx = pd.date_range("1985-01-01", "2026-04-01", freq="QS")
qg = pd.Series(0.5 * np.arange(len(qidx)) + np.sin(np.arange(len(qidx))), qidx)
qch = qg - qg.shift(4)
qref = S.reference(qch, "QS", 4, rec, 40)
qg2 = qg.copy()
qg2.iloc[-1] = qg2.iloc[-5] + qref["mean"] - 1.7 * qref["sd"]
mr = S.measure_reading("output_per_hour", sp6, {"gap": qg2, "legs": {}}, rec, set(), None)
check("S3 the statistic as specified: a synthetic gap with a known excess of 2.5 sd gives E = +2.5 (and -2.5 signed the "
      "other way); the reference is the 1990-2019 windows with no recession month, so wild values inside recessions (before "
      "the trough month, whose level starts the next normal window) leave it unchanged; a series without 1990-2019 history "
      "falls back to its own history, flagged, ending a window before the latest (the latest is not in its own benchmark); "
      "the full measure path gives E = -1.7 for a quarterly gap built to -1.7 sd",
      abs(E_up - target) < 1e-9 and abs(E_dn + target) < 1e-9 and abs(ref["mean"] - manual.mean()) < 1e-12
      and abs(ref["sd"] - manual.std(ddof=1)) < 1e-12 and ref["n"] == len(manual)
      and abs(ref_r["mean"] - ref["mean"]) < 1e-12 and abs(ref_r["sd"] - ref["sd"]) < 1e-12
      and short["own_history"] and not ref["own_history"] and short["to"] == str((short_ch.index[-1] - pd.DateOffset(months=12)).date())[:7]
      and abs(mr["reading"]["E_signed"] + 1.7) < 1e-9 and mr["reading"]["zone"] == "-",
      f"E {E_up:+.6f} / {E_dn:+.6f}; reference n {ref['n']} (manual {len(manual)}); short history own={short['own_history']} "
      f"to {short['to']}; quarterly E {mr['reading']['E_signed']:+.4f}")

# S4 recession dating from USREC
usrec = ALL["USREC"]
rm = sorted(m for m in S.recession_months(usrec) if pd.Timestamp("1990-01-01") <= m < pd.Timestamp("2021-01-01"))
rm_later = sorted(m for m in S.recession_months(usrec) if m >= pd.Timestamp("2021-01-01"))
nber = (list(pd.date_range("1990-08-01", "1991-03-01", freq="MS")) + list(pd.date_range("2001-04-01", "2001-11-01", freq="MS"))
        + list(pd.date_range("2008-01-01", "2009-06-01", freq="MS")) + list(pd.date_range("2020-03-01", "2020-04-01", freq="MS")))
wm_m = S.window_months("2026-09-01", "MS", 12)
wm_q = S.window_months("2026-04-01", "QS", 4)
recset = S.recession_months(usrec)
care = next(m for m in J["measures"] if m["key"] == "care")
pay_gap = S.build(ALL)
cg = pay_gap["care"]["gap"]
cch = cg - cg.shift(12)
n_manual = sum(1 for t in cch.dropna().index if pd.Timestamp("1990-01-01") <= t <= pd.Timestamp("2019-12-31")
               and not any(m in recset for m in pd.date_range(t - pd.DateOffset(months=11), t, freq="MS")))
check("S4 recessions are NBER's (FRED USREC): 1990-2020 the recession months are exactly Aug 1990-Mar 1991, Apr-Nov 2001, "
      "Jan 2008-Jun 2009 and Mar-Apr 2020; a 12-month window ending September covers October-September, a 4-quarter window "
      "ending in Q2 covers July-June; measure 1's reference holds exactly the 1990-2019 windows that touch none of them",
      rm == nber and wm_m[0] == pd.Timestamp("2025-10-01") and wm_m[-1] == pd.Timestamp("2026-09-01") and len(wm_m) == 12
      and wm_q[0] == pd.Timestamp("2025-07-01") and wm_q[-1] == pd.Timestamp("2026-06-01") and len(wm_q) == 12
      and care["reference"]["n"] == n_manual,
      f"{len(rm)} recession months 1990-2020; dated since: {[str(m.date())[:7] for m in rm_later] or 'none'}; "
      f"measure 1 reference n {care['reference']['n']} (manual {n_manual})")

# S5 the dispersion benchmark against the panel (24-month windows), and the tracker's own (12-month windows)
PANEL_REC = [("1990-07-01", "1991-03-01"), ("2001-03-01", "2001-11-01"), ("2007-12-01", "2009-06-01"), ("2020-02-01", "2020-04-01")]
PANEL_SIDS = sorted(list(S.UNITS.values()) + ["PAYEMS"])


def vintage_hash(folder):
    h = hashlib.sha256()
    for sid in PANEL_SIDS:
        h.update(open(os.path.join(folder, sid + ".csv"), "rb").read().replace(b"\r\n", b"\n"))
    return h.hexdigest()


# The panel's inputs are paths/cache's payroll files of 2026-10-12, which other units (baumol.py) may refresh: pinned
# by hash, the reproduction is tested on them and reported on any later vintage.
PANEL_INPUTS_2026_10_12 = "5903e62eed944114278db839b973d8cd5becde4a530cacf0d2aa831412ba4742"
panel_same = vintage_hash(os.path.join(ROOT, "cache")) == PANEL_INPUTS_2026_10_12
old = {sid: cached(sid, os.path.join(ROOT, "cache")) for sid in PANEL_SIDS}
new = {sid: ALL[sid] for sid in PANEL_SIDS}
aug = pd.Timestamp("2026-08-01")
Dp = S.dispersion(old, recset, PANEL_REC, H=24)          # the panel's inputs and its recession rule
Do = S.dispersion(old, recset, H=24)                     # the panel's inputs, NBER dating
Dn = S.dispersion(new, recset, H=24)                     # this vintage, NBER dating
Dnp = S.dispersion(new, recset, PANEL_REC, H=24)
panel = {"median": 0.4, "p95": 17.9, "recession": 55.7, "aug2026": 27.7}
got = {"median": Dp["normal_median"], "p95": Dp["normal_p95"], "recession": Dp["recession_median_pre2020"], "aug2026": float(Dp["share"][aug])}
check("S5a the panel's 2,047-cut benchmark (24-month windows) is reproduced on its own inputs with its recession rule: "
      "normal-month median 0.4%, 95th percentile 17.9%, recessions 55.7%, August 2026 27.7%; 2,047 cuts; the twelve units sum "
      "to total payrolls (tested while paths/cache holds the panel's inputs, pinned by hash; reported on a later vintage)",
      (not panel_same or all(abs(got[k] - panel[k]) <= 0.06 for k in panel)) and Dp["n_cuts"] == 2047
      and Dp["sum_vs_payems_max_abs_pct"] < 0.1,
      f"{ {k: round(v, 2) for k, v in got.items()} }; inputs {'the panel’s (tested)' if panel_same else 'refreshed since (reported only)'}")
VINTAGE_2026_10_12 = "db8690e1e6da365f3410eae70daa9fc4d00309882b7df91380173beb14072b46"
same_vintage = vintage_hash(S.CACHE) == VINTAGE_2026_10_12
rev_n, rev_p = float(Dn["share"][aug] - Do["share"][aug]), float(Dnp["share"][aug] - Dp["share"][aug])
check("S5b on 24-month windows the tracker's dating differs from the panel's for a stated reason: NBER dating (USREC) counts "
      "5 more months as normal than the panel's hand-typed peaks, which moves the 95th percentile from 17.9% to 18.7% on "
      "the panel's inputs; on the 2026-10-12 vintage the September 2026 release's revisions move August 2026 by 1-3 points "
      "(on later vintages reported, not tested)",
      (not panel_same or (abs(Do["normal_p95"] - 18.69) < 0.05 and Do["n_normal_months"] - Dp["n_normal_months"] == 5))
      and (not (same_vintage and panel_same) or (abs(Dn["normal_p95"] - Do["normal_p95"]) < 0.05 and 1.0 < rev_n < 3.0 and 1.0 < rev_p < 3.0)),
      f"p95: panel rule {Dp['normal_p95']:.2f}, NBER on the panel's inputs {Do['normal_p95']:.2f}, NBER on this vintage "
      f"{Dn['normal_p95']:.2f}; normal months {Dp['n_normal_months']} vs {Do['n_normal_months']}; Aug 2026: {Dp['share'][aug]:.2f} "
      f"(panel) -> {Do['share'][aug]:.2f} (NBER dating) -> {Dn['share'][aug]:.2f} (revised data)")

# S5c measure 2 as judged: 12-month windows, so a judged reading holds nothing from before its window's start
D12 = S.dispersion(ALL, recset)
b2 = pd.Timestamp("2024-09-01")
pert = {sid: s.astype(float).copy() for sid, s in ALL.items()}
rng = np.random.default_rng(7)
for sid in S.UNITS.values():
    m_ = pert[sid].index < b2
    pert[sid][m_] = pert[sid][m_] * np.exp(rng.normal(0, 0.05, m_.sum()))
Dpert = S.dispersion(pert, recset, moments=D12["_moments"])
e2 = b2 + pd.DateOffset(months=12)
rce = J["dispersion_recovery_effect"]
check("S5c measure 2 is judged on 12-month growth with frozen per-cut moments: changing every payroll figure before a window's "
      "start leaves the share at its end unchanged (and moves the share at its start), so no already-seen month enters a "
      "judged reading and consecutive windows share no data; the tracker's threshold and latest share are the results'; "
      "the share of the threshold set by the year after a recession's exclusion is reported",
      abs(Dpert["share"][e2] - D12["share"][e2]) < 1e-12 and abs(Dpert["share"][b2] - D12["share"][b2]) > 0
      and D12["window_months"] == 12 and abs(D12["normal_p95"] - J["dispersion_benchmark"]["normal_p95"]) < 1e-9
      and J["dispersion_benchmark"]["window_months"] == 12 and J["measures"][1]["reference"]["from"] == D12["normal_from"]
      and rce["normal_months_at_or_above_p95"] >= rce["of_which_in_the_year_after_a_recession_exclusion"],
      f"share at {str(e2.date())[:7]} {D12['share'][e2]:.2f} either way; at {str(b2.date())[:7]} {D12['share'][b2]:.2f} -> "
      f"{Dpert['share'][b2]:.2f}; p95 {D12['normal_p95']:.2f} (normal months from {D12['normal_from']}); "
      f"{rce['of_which_in_the_year_after_a_recession_exclusion']} of {rce['normal_months_at_or_above_p95']} months at or above "
      f"it fall in the year after a recession's exclusion (without those years: {rce['p95_without_those_recovery_years']:.1f}%)")

# S6 the freeze judges only what comes after the baseline
b_date = pd.Timestamp("2024-09-01")
jw = S.judged_windows(gap, b_date, 12, ref, +1)
gap_pre = gap.copy()
gap_pre[gap_pre.index < b_date] += 7.0 * np.cos(np.arange((gap_pre.index < b_date).sum()))
jw_pre = S.judged_windows(gap_pre, b_date, 12, ref, +1)
gap_post = gap.copy()
gap_post[gap_post.index > b_date + pd.DateOffset(months=6)] += 3.0
jw_post = S.judged_windows(gap_post, b_date, 12, ref, +1)
manual_E = (gap[pd.Timestamp("2025-09-01")] - gap[b_date] - ref["mean"]) / ref["sd"]
share = pd.Series(np.r_[np.full(30, 25.0), np.full(15, 10.0)], pd.date_range("2023-01-01", periods=45, freq="MS"))
jd = S.judged_dispersion(share, "2024-01-01", 18.7)
check("S6 the freeze judges only observations after the baseline: windows start at the baseline's last observation, run "
      "12 months apart without overlap, and only complete windows count; changing every value before the baseline leaves the "
      "judged E unchanged, changing values after it does not; measure 2's windows read + while at or above the frozen 95th "
      "percentile and - once the share has fallen below it",
      [w["start"] for w in jw] == ["2024-09-01", "2025-09-01"][:len(jw)] and len(jw) == 2 and jw[1]["end"] == "2026-09-01"
      and all(pd.Timestamp(w["start"]) >= b_date for w in jw)
      and all(abs(a["E_signed"] - b["E_signed"]) < 1e-12 for a, b in zip(jw, jw_pre))
      and abs(jw_post[0]["E_signed"] - jw[0]["E_signed"]) > 1 and abs(jw[0]["E_signed"] - manual_E) < 1e-12
      and S.judged_windows(gap, "2026-01-01", 12, ref, +1) == [] and [w["zone"] for w in jd] == ["+", "-"],
      f"windows {[(w['start'], w['end'], round(w['E_signed'], 3)) for w in jw]}; dispersion windows {[(w['start'], w['end'], w['zone']) for w in jd]}")

# S7 the freeze states (on a scratch baseline path, so the real working copy, once written, does not enter)
tmp7 = tempfile.mkdtemp(prefix="splits_check_")
git_real, baseline_real = S._git, S.BASELINE
code_hash = S.file_hash(os.path.join(ROOT, "code", "splits.py"))
fake_bl = {"definitions_sha256": S.definitions_hash(), "protocol_sha256": S.file_hash(S.PROTOCOL), "code_sha256": code_hash,
           "written_utc": "2026-10-20T07:00:00Z"}
try:
    S.BASELINE = os.path.join(tmp7, "none.json")
    st0, _ = S.freeze_state(tag_exists=False, baseline=None)
    st1, _ = S.freeze_state(tag_exists=True, baseline=None, tag_date="2026-10-20")
    st2, _ = S.freeze_state(tag_exists=False, baseline=fake_bl)
    st3, _ = S.freeze_state(tag_exists=True, baseline=fake_bl, tag_date="2026-10-20T10:00:00+02:00")
    st4, _ = S.freeze_state(tag_exists=True, baseline={**fake_bl, "definitions_sha256": "0" * 64}, tag_date="2026-10-20")
    st8, _ = S.freeze_state(tag_exists=True, baseline={**fake_bl, "code_sha256": "0" * 64}, tag_date="2026-10-20T10:00:00+02:00")
    st9, _ = S.freeze_state(tag_exists=True, baseline=fake_bl, tag_date="2026-10-24T10:00:00+02:00")
    # through git: the tagged commit's baseline is used, a differing working copy is flagged, a tag without one judges nothing
    tagged = {**fake_bl, "written_utc": "2026-10-20T07:30:00Z"}
    S.BASELINE = os.path.join(tmp7, "working.json")
    json.dump({**fake_bl, "written_utc": "2026-10-21T00:00:00Z"}, open(S.BASELINE, "w", encoding="utf-8"))
    S._git = lambda *a: (S.TAG if a[:2] == ("tag", "-l") else "abc123" if a[0] == "rev-list" else
                         "2026-10-20T10:00:00+02:00" if a[0] in ("log", "for-each-ref")
                         else json.dumps(tagged) if a[:2] == ("show", f"{S.TAG}:{S.BASELINE_IN_REPO}") else None)
    st5, bl5 = S.freeze_state()
    st10, _ = S.freeze_state(previous={"status": {"tag_commit": "def456"}})
    S._git = lambda *a: (S.TAG if a[:2] == ("tag", "-l") else "2026-10-20T10:00:00+02:00" if a[0] == "log" else None)
    st6, bl6 = S.freeze_state()
    S._git = lambda *a: None
    st7, bl7 = S.freeze_state()
    S._git = lambda *a: S.TAG if a[:2] == ("tag", "-l") else None
    try:
        S.write_baseline({}, {}, {})
        refused_rewrite = False
    except SystemExit:
        refused_rewrite = True
finally:
    S._git, S.BASELINE = git_real, baseline_real
unfrozen_now = True if J["status"]["tag_exists"] else (
    (not J["status"]["frozen"]) and J["judged"] == []
    and all(m["judged_windows"] is None and S.UNFROZEN_LABEL in m["status"] for m in J["measures"]))
check("S7 the freeze states: no tag and no baseline -> every reading 'starting point (already seen; not judged)' (and so in "
      "today's results); a tag without a baseline, or a baseline without a tag, judges nothing; tag and baseline -> judged; "
      "definitions (with their code) that differ from the baseline's -> a deviation; a changed code file -> labelled; a tag "
      "made more than a day after the baseline -> flagged; once tagged, the baseline is the one in the tagged commit (a "
      "working copy edited later is flagged, not used), the tagged commit's SHA is recorded and a tag that has moved since "
      "the last run is flagged; a tagged commit without a baseline judges nothing; the baseline cannot be rewritten once the "
      "tag exists",
      st0["label"] == S.UNFROZEN_LABEL and not st0["frozen"] and not st1["frozen"] and not st2["frozen"] and st3["frozen"]
      and st3["definitions_match"] and st3["code_matches_baseline"] and "deviation" not in st3["label"] and not st3["flags"]
      and st3["label"] == S.FROZEN_LABEL
      and st4["frozen"] and "deviation" in st4["label"] and st8["code_matches_baseline"] is False and "code has changed" in st8["label"]
      and st9["tag_days_after_baseline"] > 1 and st9["flags"] and "days after the baseline" in st9["label"]
      and st5["frozen"] and st5["baseline_source"] == "tagged commit" and bl5["written_utc"] == "2026-10-20T07:30:00Z"
      and st5["baseline_working_copy_differs"] is True and st5["tag_date"].startswith("2026-10-20") and st5["tag_commit"] == "abc123"
      and st10["tag_moved_since_last_run"] is True and "moved" in st10["label"]
      and not st6["frozen"] and "not judged" in st6["label"]
      and not st7["frozen"] and st7["baseline_source"] == "working copy" and st7["label"].endswith(S.UNFROZEN_LABEL)
      and refused_rewrite and unfrozen_now,
      f"labels: {st0['label']!r} | {st3['label']!r} | {st4['label']!r} | {st8['label']!r} | {st9['label']!r} | "
      f"git, tagged: source {st5['baseline_source']}, commit {st5['tag_commit']}, working copy differs "
      f"{st5['baseline_working_copy_differs']} | moved: {st10['flags']} | tag without baseline: {st6['label']!r}")

# S8 a whole frozen run, end to end: a baseline written on data to June 2025, then the full data judged against it
tmp = tempfile.mkdtemp(prefix="splits_check_")
SAVED_ATTRS = ("fetch", "fred_titles", "VINTAGES", "RESULTS", "BASELINE", "FIGURE", "_git", "_today", "LOOK_FILE")
saved = {k: getattr(S, k) for k in SAVED_ATTRS}
CUT = pd.Timestamp("2025-06-30")
TAG_DATE = "2025-07-15T12:00:00+02:00"


def frozen_git(bl_path, code_src=None, look=None):
    def g(*a):
        if a[:2] == ("tag", "-l"):
            return a[2] if (a[2] == S.TAG or (look and a[2] == look[0])) else None
        if a[0] in ("log", "for-each-ref"):
            return TAG_DATE
        if a[0] == "rev-list":
            return "f" * 40
        if a[:2] == ("show", f"{S.TAG}:{S.BASELINE_IN_REPO}"):
            return open(bl_path, encoding="utf-8").read()
        if a[:2] == ("show", f"{S.TAG}:{S.CODE_IN_REPO}"):
            return code_src
        if look and a[0] == "show" and a[1].startswith(look[0] + ":"):
            return json.dumps(look[1])
        return None
    return g


def run_main(args, today):
    S._today = lambda: today
    with contextlib.redirect_stdout(io.StringIO()):
        return S.main(args)


try:
    S.VINTAGES, S.RESULTS = os.path.join(tmp, "v.json"), os.path.join(tmp, "r.json")
    S.BASELINE, S.FIGURE = os.path.join(tmp, "b.json"), os.path.join(tmp, "f.png")
    S.LOOK_FILE = os.path.join(tmp, "look_{year}.json")
    S.fred_titles = lambda refresh=False: {}
    S.fetch = lambda sid, refresh=False, vint=None: ALL[sid][lambda s: s.index <= CUT]
    S._git = lambda *a: None
    run_main(["--write-baseline"], dt.date(2025, 7, 15))
    BL = json.load(open(S.BASELINE, encoding="utf-8"))
    S.fetch = lambda sid, refresh=False, vint=None: ALL[sid]
    S._git = frozen_git(S.BASELINE)
    R_before = run_main([], dt.date(2026, 10, 13))
    R = run_main([], dt.date(2026, 11, 16))
finally:
    for k, v in saved.items():
        setattr(S, k, v)
ok8, rows = True, []
B_frozen = S.build(ALL, BL["fits"])
for m in R["measures"]:
    fb = BL["measures"][m["key"]]
    w = (m["judged_windows"] or [None])[0]
    if w is None or w["start"] != fb["last_obs"] or m["status"] != "judged":
        ok8 = False
        rows.append((m["id"], m["status"], w))
        continue
    if m["key"] != "payroll_dispersion":
        g = B_frozen[m["key"]]["gap"]
        e = m["direction_toward_paper"] * (g[pd.Timestamp(w["end"])] - g[pd.Timestamp(w["start"])] - fb["reference"]["mean"]) / fb["reference"]["sd"]
        ok8 &= abs(e - w["E_signed"]) < 1e-9 and m["reference"]["mean"] == fb["reference"]["mean"] and w.get("zone_check", False)
        rows.append((m["id"], w["start"][:7], w["end"][:7], round(w["E_signed"], 2), w["counted_zone"], w["fits"]))
    else:
        ok8 &= abs(m["reference"]["normal_p95"] - BL["measures"]["payroll_dispersion"]["normal_p95"]) < 1e-12
        rows.append((m["id"], w["start"][:7], w["end"][:7], round(w["level"], 1), w["zone"], w["fits"]))
jd0 = R["judged"][0] if R["judged"] else {}
jb0 = R_before["judged"][0] if R_before["judged"] else {}
VERDICT_WORDS = ("supports the paper", "favours the rivals", "nothing unusual", "inconclusive",
                 "void for the paper against the cycle: a recession touches the window")
check("S8 a whole frozen run: with a baseline written on data to June 2025 and the tag present, every measure is 'judged' on "
      "exactly the windows that start at its baseline observation, with the frozen references, fitted coefficients and "
      "dispersion threshold; each judged E equals the gap's change over that window against the frozen reference; the "
      "combined reading covers the eleven counted measures (measure 4 beside) and waits for the yearly look (15 November "
      "2026 for a tag in July 2025), then returns one of the protocol's verdicts; the latest rolling readings say 'not judged'",
      ok8 and R["status"]["frozen"] and R["status"]["definitions_match"] and R["status"]["baseline_source"] == "tagged commit"
      and jd0.get("n_measures") == 11 and jd0.get("beside_the_count", {}).get("id") == 4
      and jb0.get("verdict") == "awaiting the yearly look" and jb0.get("look_date") == "2026-11-15"
      and jd0.get("verdict") in VERDICT_WORDS
      and all("not judged" in m["latest"]["label"] for m in R["measures"])
      and BL["definitions_sha256"] == S.definitions_hash() and BL["protocol_sha256"] == S.file_hash(S.PROTOCOL)
      and {m["key"]: m["extra"].get("fit") for m in R["measures"] if "fit" in m["extra"]} == BL["fits"],
      f"{rows}; combined: count {jd0.get('count')}, tally {jd0.get('tally_counts')}, verdict {jd0.get('verdict')!r} "
      f"(before the look: {jb0.get('verdict')!r}; a synthetic freeze on already-seen data: a test of the machinery, not a reading)")

# S9 a code change after the tag: the tagged code is run beside the working code; its judged readings stand, and any
# difference is labelled a deviation (a change that leaves them unchanged is labelled as such)
code_now = open(os.path.join(ROOT, "code", "splits.py"), encoding="utf-8").read()
old_zone = 'return "+" if e >= 1 else ("-" if e <= -1 else "0")'
code_half = code_now.replace(old_zone, 'return "+" if e >= 0.5 else ("-" if e <= -0.5 else "0")')
code_comment = code_now.replace("def summary(res: dict):", "def summary(res: dict):  # (edited after the freeze)", 1)
bl_other = os.path.join(tmp, "b_other.json")
json.dump({**BL, "code_sha256": "0" * 64}, open(bl_other, "w", encoding="utf-8"))
saved = {k: getattr(S, k) for k in SAVED_ATTRS}
try:
    S.VINTAGES, S.RESULTS = os.path.join(tmp, "v.json"), os.path.join(tmp, "r9.json")
    S.BASELINE, S.FIGURE = os.path.join(tmp, "b9.json"), os.path.join(tmp, "f.png")
    S.fred_titles = lambda refresh=False: {}
    S.fetch = lambda sid, refresh=False, vint=None: ALL[sid]
    S._git = frozen_git(bl_other, code_half)
    R9 = run_main([], dt.date(2026, 11, 16))
    S._git = frozen_git(bl_other, code_comment)
    R9b = run_main([], dt.date(2026, 11, 16))
    S._git = frozen_git(bl_other, code_half)
    T9 = S.tagged_code()
finally:
    for k, v in saved.items():
        setattr(S, k, v)
half_zones = [(w["E_signed"], w["zone"]) for m in R9["measures"] if m["key"] != "payroll_dispersion" for w in (m["judged_windows"] or [])]
half_ok = all(z == ("+" if e >= 0.5 else ("-" if e <= -0.5 else "0")) for e, z in half_zones)
check("S9 a code change after the fixed date: the tagged code is run on the same data beside the working code; when they "
      "judge differently the tagged code's readings are the judged ones, the working code's are reported beside them and "
      "the run is labelled a deviation; a change that leaves every judged reading unchanged is labelled so; editing a "
      "measure-defining function changes the definitions hash",
      R9["status"]["code_matches_baseline"] is False and "deviation" in R9["status"]["label"] and R9["status"]["code_deviation"]
      and half_ok and "judged_working_code" in R9 and any(m.get("judged_windows_working_code") for m in R9["measures"])
      and "unchanged" in R9b["status"]["label"] and not R9b["status"]["code_deviation"] and "deviation" not in R9b["status"]["label"]
      and T9.definitions_hash() != S.definitions_hash(),
      f"{len(R9['status']['code_deviation'])} differences, e.g. {R9['status']['code_deviation'][:2]}; comment-only change: "
      f"{R9b['status']['label'][-80:]!r}")

# S10 the yearly look: a tagged look stands; later runs report the same window on revised data beside it
look_obj = {"window": 1, "look_date": "2026-11-15", "written_utc": "2026-11-16T09:00:00Z",
            "combined": {**jd0, "verdict": "favours the rivals", "count": -5}}
saved = {k: getattr(S, k) for k in SAVED_ATTRS}
refused_look = []
try:
    S.VINTAGES, S.RESULTS = os.path.join(tmp, "v.json"), os.path.join(tmp, "r10.json")
    S.BASELINE, S.FIGURE = os.path.join(tmp, "b10.json"), os.path.join(tmp, "f.png")
    S.LOOK_FILE = os.path.join(tmp, "look_{year}.json")
    S.fred_titles = lambda refresh=False: {}
    S.fetch = lambda sid, refresh=False, vint=None: ALL[sid]
    S._git = frozen_git(os.path.join(tmp, "b.json"), None,
                        ("paths-splits-look-2026", look_obj))
    R10 = run_main([], dt.date(2026, 11, 20))
    for args, today in ((["--look"], dt.date(2026, 11, 20)), (["--refresh", "--look"], dt.date(2026, 10, 13))):
        try:
            S._git = frozen_git(os.path.join(tmp, "b.json"))
            run_main(args, today)
            refused_look.append(False)
        except SystemExit:
            refused_look.append(True)
    S._git = frozen_git(os.path.join(tmp, "b.json"))
    run_main(["--refresh", "--look"], dt.date(2026, 11, 20))
    LK = json.load(open(os.path.join(tmp, "look_2026.json"), encoding="utf-8"))
finally:
    for k, v in saved.items():
        setattr(S, k, v)
j10 = R10["judged"][0]
check("S10 the yearly look: once tagged, its verdict stands and the same window on today's data is reported beside it as "
      "'on revised data'; the look refuses without a fresh vintage (--refresh) and before its date, and writes the window's "
      "combined reading, per-measure readings and vintages",
      j10["verdict"] == "favours the rivals" and j10.get("verdict_on_revised_data") == jd0.get("verdict")
      and j10["look"]["tag"] == "paths-splits-look-2026" and refused_look == [True, True]
      and LK["window"] == 1 and LK["combined"]["verdict"] == jd0.get("verdict") and len(LK["measures"]) == 12,
      f"tagged verdict {j10['verdict']!r}, on revised data {j10.get('verdict_on_revised_data')!r}; refusals {refused_look}")

# S11 a failed refresh keeps the previous vintage and its record, warns, and stops a baseline or a look
tmp11 = tempfile.mkdtemp(prefix="splits_check_")
shutil.copy(os.path.join(S.CACHE, "UNRATE.csv"), os.path.join(tmp11, "UNRATE.csv"))
v11 = {"UNRATE": dict(json.load(open(S.VINTAGES, encoding="utf-8"))["UNRATE"])}
before = dict(v11["UNRATE"])
saved = {k: getattr(S, k) for k in SAVED_ATTRS + ("CACHE",)}
pull_real = S._lc.pull_fred
err11 = io.StringIO()
try:
    S.CACHE = tmp11
    S._lc.pull_fred = lambda sid: None
    S.REFRESH_FAILED.clear()
    with contextlib.redirect_stderr(err11):
        s11 = S.fetch("UNRATE", refresh=True, vint=v11)
    failed11 = list(S.REFRESH_FAILED)
    kept = open(os.path.join(tmp11, "UNRATE.csv")).read() == open(os.path.join(S.CACHE, "UNRATE.csv")).read()
    # a whole run that asks for a baseline on a failed refresh is refused, writing no baseline
    for sid in S.MANIFEST:
        shutil.copy(os.path.join(saved["CACHE"], sid + ".csv"), os.path.join(tmp11, sid + ".csv"))
    S.VINTAGES, S.RESULTS = os.path.join(tmp11, "v.json"), os.path.join(tmp11, "r.json")
    S.BASELINE, S.FIGURE = os.path.join(tmp11, "b.json"), os.path.join(tmp11, "f.png")
    S.fred_titles = lambda refresh=False: {}
    S._git = lambda *a: None
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            run_main(["--refresh", "--write-baseline"], dt.date(2026, 10, 13))
        refused11 = False
    except SystemExit:
        refused11 = True
finally:
    S._lc.pull_fred = pull_real
    for k, v in saved.items():
        setattr(S, k, v)
rec11 = v11["UNRATE"]
check("S11 a failed refresh keeps the previous file and its vintage record (download date and hash unchanged), marks it "
      "refresh_failed_utc, warns, and refuses to write a baseline (or a look) on that vintage",
      kept and failed11 == ["UNRATE"] and rec11["downloaded_utc"] == before["downloaded_utc"] and rec11["sha256"] == before["sha256"]
      and rec11.get("refresh_failed_utc") and "refresh failed" in err11.getvalue() and refused11
      and not os.path.exists(os.path.join(tmp11, "b.json")) and len(s11) > 100,
      f"record kept ({rec11['downloaded_utc']}, {rec11['sha256'][:12]}), refresh_failed_utc {rec11.get('refresh_failed_utc')}; "
      f"baseline refused {refused11}")

# S12 the conditions on the rivals' calls, and which explanation a reading fits
fed = S.fed_target(ALL)
rr = ALL["REAINTRATREARAT10Y"]
cases = {
    "cut 2019": S.rate_cut(fed, "2019-12-01", "MS") is True,          # 1.75 against 2.50
    "cut 2024Q4": S.rate_cut(fed, "2024-10-01", "QS") is True,        # December 2024 4.50 against December 2023 5.50
    "no cut 2018": S.rate_cut(fed, "2018-12-01", "MS") is False,      # hikes
    "target 2008 joins": abs(fed[pd.Timestamp("2008-11-01")] - 1.0) < 1e-9 and abs(fed[pd.Timestamp("2009-01-01")] - 0.25) < 1e-9,
    "hiring - without a cut: neither": S.fits_of("hiring", {"zone": "-", "gap": 0.1, "cond": {"rate_cut": False}}) == [],
    "hiring - after a cut: rival": S.fits_of("hiring", {"zone": "-", "gap": 0.1, "cond": {"rate_cut": True}}) == ["rival"],
    "build-out - without a cut: neither": S.fits_of("build_out", {"zone": "-", "cond": {"rate_cut": None}}) == [],
    "land - with real rates not rising: neither": S.fits_of("site_rent", {"zone": "-", "cond": {"real_rate_rose": False}}) == [],
    "land - with real rates rising: rival": S.fits_of("site_rent", {"zone": "-", "cond": {"real_rate_rose": True}}) == ["rival"],
    "saving 0 during the build-out: neither": S.fits_of("saving", {"zone": "0", "cond": {"build_out_turned": False}}) == [],
    "saving 0 after it turns: rival": S.fits_of("saving", {"zone": "0", "cond": {"build_out_turned": True}}) == ["rival"],
    "transformers below base at the deadline: paper": S.fits_of("transformer_premium", {"zone": "0", "cond": {"deadline": {"base": 10.0, "level": 9.0}}}) == ["paper"],
    "transformers above base at the deadline: rival": S.fits_of("transformer_premium", {"zone": "0", "cond": {"deadline": {"base": 10.0, "level": 11.0}}}) == ["rival"],
    "null fits are not signed": not S.rival_signed("output_per_hour", {"zone": "0", "fits": ["rival"]})
                                and not S.rival_signed("payroll_dispersion", {"zone": "0", "fits": ["rival"]})
                                and S.rival_signed("payroll_dispersion", {"zone": "-", "fits": ["rival"]}),
    "real rate 2022Q4 rose": S.real_rate_rose(rr, "2022-10-01", "QS", 4) is True,
}
lat = {m["key"]: m["latest"] for m in J["measures"]}
cases["the results apply them"] = (lat["hiring"]["cond"]["rate_cut"] == S.rate_cut(fed, lat["hiring"]["date"], "MS")
                                   and lat["saving"]["cond"]["build_out_turned"] == (lat["build_out"]["zone"] == "-"))
check("S12 the rivals' conditions are tested, not assumed: a rate cut is the fed funds target (DFEDTAR to December 2008, "
      "then the range's upper limit) at least 50 bp below its level twelve months earlier, and without one a fall in hiring's "
      "gap or the build-out fits neither; land falling fits the real-rate rival only when the real rate rose; saving's 'no "
      "change' fits the wealth effect only once the build-out has turned; transformers are judged on their level at the "
      "deadline; 'nothing unusual' fits are not signed calls",
      all(cases.values()), {k: v for k, v in cases.items() if not v} or f"{len(cases)} cases")

# S13 recessions: measure 2's window is its own 12 months (and, for a '-', the 12 before its start); measures 3 and 7 are
# judged in a recession, the others void
ctx13 = {"D": {"share": pd.Series([30.0] * 13 + [10.0] * 12 + [30.0] * 12, pd.date_range("2000-01-01", periods=37, freq="MS"))},
         "p95": 20.0, "anyrec": {pd.Timestamp("2000-06-01")}, "rec": set(), "S": {}}
r13a = S.reading_at("payroll_dispersion", "2001-02-01", ctx13)   # 30 (Feb 2000) -> 10: '-'; its window holds June 2000
r13b = S.reading_at("payroll_dispersion", "2002-02-01", ctx13)   # 10 -> 30: '+'; window Mar 2001-Feb 2002, clean
ctx13["anyrec"] = {pd.Timestamp("1999-06-01")}
r13c = S.reading_at("payroll_dispersion", "2001-02-01", ctx13)   # '-' whose start's window (Mar 1999-Feb 2000) holds June 1999
gq = pd.Series(np.arange(40, dtype=float), pd.date_range("1995-01-01", periods=40, freq="QS"))
ctxq = {"S": {k: {"E": gq * 0 + 1.5, "gap": gq, "legs": {}} for k in ("graduates", "labour_share", "site_rent")},
        "anyrec": {pd.Timestamp("2001-06-01")}, "rec": set(), "rr": pd.Series(dtype=float), "fed": pd.Series(dtype=float)}
S.SPEC["graduates"]["freq"], keep_freq = "QS", S.SPEC["graduates"]["freq"]
S.SPEC["graduates"]["k"], keep_k = 4, S.SPEC["graduates"]["k"]
try:
    rq = {k: S.reading_at(k, "2001-10-01", ctxq) for k in ("graduates", "labour_share", "site_rent")}
finally:
    S.SPEC["graduates"]["freq"], S.SPEC["graduates"]["k"] = keep_freq, keep_k
check("S13 recessions: measure 2's reading is touched by a recession or Sahm month in its own 12 months, and a fall below "
      "the threshold also by one in the 12 months before its start; graduates and the labour share are still judged in a "
      "recession window (their rival is the cycle), every other measure is void; the combined verdict is void either way",
      r13a["zone"] == "-" and r13a["recession_in_window"] and r13b["zone"] == "+" and not r13b["recession_in_window"]
      and r13c["zone"] == "-" and r13c["recession_in_window"]
      and all(r["recession_in_window"] for r in rq.values()) and not rq["graduates"]["void"] and not rq["labour_share"]["void"]
      and rq["site_rent"]["void"]
      and S.verdict(5, {"paper": 9, "rival": 0}, {"p90": 1, "median": 0}, True).startswith("void"),
      f"measure 2: {r13a['zone']}/{r13a['recession_in_window']}, {r13b['zone']}/{r13b['recession_in_window']}, "
      f"{r13c['zone']}/{r13c['recession_in_window']}; void: { {k: r['void'] for k, r in rq.items()} }")

# S14 the results schema
T = {"schema_version": int, "generated_utc": str, "protocol": str, "definitions_sha256": str, "protocol_sha256": str, "status": dict,
     "recession": dict, "statistic": dict, "measures": list, "dispersion_benchmark": dict, "dispersion_recovery_effect": dict,
     "dispersion_path": dict, "combined": dict, "judged": list, "base_rates": dict, "channels": dict, "watch": list,
     "context": dict, "refresh_failed": list, "vintages": dict}
TM = {"id": int, "key": str, "name": str, "paper_call": str, "rival_name": str, "rival_call": str, "fits_rule": str, "series": list,
      "transformation": str, "legs_defined": dict, "frequency": str, "window": str, "direction_toward_paper": int, "status": str,
      "in_count": bool, "judged_in_recessions": bool,
      "latest": dict, "legs": dict, "reference": dict, "base_rates": dict, "carry_forward": dict, "judged_windows": (list, type(None)),
      "thresholds_plain": dict, "extra": dict, "plain": dict, "history": dict}
TL = {"date": str, "gap": float, "change": (float, type(None)), "E_signed": (float, type(None)), "E": (float, type(None)),
      "zone": str, "fits": list, "counted_zone": str, "reading": str, "label": str, "recession_in_window": bool, "void": bool,
      "rival_signed": bool, "cond": dict, "change_since_2019": (float, type(None))}
TW = {"key": str, "name": str, "series": list, "note": str, "date": str, "level": float, "units": str}
TS = {"tag": str, "tag_exists": bool, "frozen": bool, "label": str, "baseline_exists": bool, "flags": list}
TC = {"today_all_12": int, "today_with_1990_2019_history": int, "today": dict, "beside_the_count": dict, "normal_years": dict,
      "by_year": dict, "historical_verdicts": dict, "tally": dict, "tally_counts": dict}
errs = []


def conform(obj, spec, where):
    for k, t in spec.items():
        if k not in obj:
            errs.append(f"{where}.{k} missing")
        elif not isinstance(obj[k], t) or (t is int and isinstance(obj[k], bool)):
            errs.append(f"{where}.{k} is {type(obj[k]).__name__}")


conform(J, T, "root")
conform(J["status"], TS, "status")
conform(J["combined"], TC, "combined")
for m in J["measures"]:
    conform(m, TM, f"measure{m.get('id')}")
    conform(m["latest"], TL, f"measure{m.get('id')}.latest")
    conform(m["history"], {"dates": list, "values": list}, f"measure{m.get('id')}.history")
for w in J["watch"]:
    conform(w, TW, f"watch.{w.get('key')}")
conform(J["context"]["wealth"], {"date": str, "top1_pct": float, "top1_is_series_high": bool, "top10_pct": float,
                                 "top10_peak": list, "series_start": str}, "context.wealth")
for sid, v in J["vintages"].items():
    conform(v, {"downloaded_utc": str, "sha256": str, "first": str, "last": str, "n": int}, f"vintage.{sid}")
check("S14 the results schema the website reads is stable (schema_version 1): top-level keys, each measure's fields and its "
      "latest reading, the watch list, the wealth context, the vintages, with their types",
      not errs and J["schema_version"] == S.SCHEMA_VERSION == 1 and [m["id"] for m in J["measures"]] == list(range(1, 13))
      and len(J["watch"]) == len(S.WATCH_SPECS), errs[:8] or f"{len(J['measures'])} measures, {len(J['watch'])} watch items")

# S15 the watch list is never judged; the count holds the eleven measures with 1990-2019 history, measure 4 beside it
forbidden = {"E", "E_signed", "zone", "fits", "counted_zone", "reading"}
tl = J["combined"]["tally"]
tally_ids = sorted(i for k in ("paper", "rival", "both", "neither") for i in tl[k])
cz = [m["latest"]["counted_zone"] for m in J["measures"]]
hist_ids = J["combined"]["measures_with_1990_2019_history"]
cz_h = [m["latest"]["counted_zone"] for m in J["measures"] if m["id"] in hist_ids]
check("S15 the watch list is reported, never judged (no E, zone or fit on any watch item); the tally places each of the "
      "twelve exactly once; today's count is the counted zones' sum (+ minus -) over the eleven measures with 1990-2019 "
      "history (all but 4, which is reported beside it), and on all twelve for reference",
      all(not (forbidden & set(w)) for w in J["watch"]) and tally_ids == list(range(1, 13)) and hist_ids == [i for i in range(1, 13) if i != 4]
      and J["combined"]["today_all_12"] == cz.count("+") - cz.count("-")
      and J["combined"]["today_with_1990_2019_history"] == cz_h.count("+") - cz_h.count("-") == J["combined"]["today"]["count"]
      and J["combined"]["beside_the_count"]["id"] == 4,
      f"tally {J['combined']['tally_counts']}; count {J['combined']['today_with_1990_2019_history']} (eleven), "
      f"{J['combined']['today_all_12']} (all twelve)")

# S16 the count's benchmark: like for like
by = J["combined"]["by_year"]
ny = J["combined"]["normal_years"]
bench = [int(y) for y, v in by.items() if v["in_benchmark"]]
counts = [by[str(y)]["count"] for y in bench]
nber_years = sorted(int(y) for y, v in by.items() if v["recession"] and int(y) <= 2019)
sahm_set = {pd.Timestamp(t) for t, v in ALL["SAHMREALTIME"].items() if v >= 0.5}
manual_void = []
for y, v in by.items():
    mo = ny["benchmark_months"]
    hit = any(S.touches(pd.Timestamp(year=int(y), month=mo[str(S.SPEC[k]["id"])], day=1), S.SPEC[k]["freq"], S.SPEC[k]["k"],
                        recset | sahm_set) for k in S.COUNT_KEYS)
    manual_void.append(hit == v["void"] or not v["complete"] or (v["void"] and v["zones"].get("2") == "-"))
check("S16 the count's benchmark is built like the judged count: the same eleven measures, every benchmark year complete "
      "(so from 2002, when hiring's history begins), each measure's window ending in the calendar month its judged windows "
      "end in, and the same void rule (an NBER recession month or a real-time Sahm reading >= 0.5 in any window); median and "
      "90th percentile as reported",
      all(by[str(y)]["n_measures"] == 11 and by[str(y)]["complete"] and not by[str(y)]["void"] and y <= 2019 for y in bench)
      and all(v["count"] == v["paper"] - v["other"] for v in by.values() if v["complete"]) and all(manual_void)
      and ny["n"] == len(bench) and ny["median"] == float(np.median(counts)) and abs(ny["p90"] - float(np.quantile(counts, 0.9))) < 1e-12
      and {1990, 1991, 2001, 2008, 2009} <= set(nber_years),
      f"{len(bench)} benchmark years {bench[0]}-{bench[-1]}: median {np.median(counts)}, p90 {np.quantile(counts, 0.9)}, range "
      f"{min(counts)} to {max(counts)}; NBER years {nber_years}")

# S17 the verdict rules, the rules in history, and the channels
hv = J["combined"]["historical_verdicts"]
nrm = {"p90": ny["p90"], "median": ny["median"]}
v_ok = all(S.verdict(by[y]["count"], by[y]["tally_counts"], nrm, by[y]["void"]) == hv["by_year"][y] for y in hv["by_year"])
rules = {
    "favours needs signed calls": S.verdict(0, {"paper": 0, "rival": 4, "rival_signed": 0}, nrm, False) == "nothing unusual",
    "signed rivals favour": S.verdict(0, {"paper": 1, "rival": 3, "rival_signed": 2}, nrm, False) == "favours the rivals",
    "supports": S.verdict(int(nrm["p90"]) + 1, {"paper": 4, "rival": 2, "rival_signed": 0}, nrm, False) == "supports the paper",
    "supports needs the tally": S.verdict(int(nrm["p90"]) + 1, {"paper": 3, "rival": 2, "rival_signed": 0}, nrm, False) == "inconclusive",
}
today = J["combined"]["today"]
loo_ok = True
for chn, ids in J["channels"].items():
    keep = [i for i in hist_ids if i not in ids]
    cc = [J["measures"][i - 1]["latest"]["counted_zone"] for i in keep]
    loo_ok &= today["leave_one_channel_out"][chn]["count"] == cc.count("+") - cc.count("-")
loo_ok &= today["rests_on_channel"] == [c for c, x in today["leave_one_channel_out"].items() if x["verdict"] != today["verdict"]]
check("S17 the verdicts: 'favours the rivals' needs the rivals' signed calls; 'nothing unusual' is a count at or below the "
      "median or only null fits; 'supports the paper' needs the count above the 90th percentile and twice the rivals' fits; "
      "the rules applied to every year reproduce the reported historical verdicts; each channel left out recomputes the "
      "count, and a verdict that flips is reported as resting on that channel",
      v_ok and all(rules.values()) and loo_ok and hv["n_benchmark_years"] == len(bench),
      f"benchmark years {hv['benchmark_years']}; retirement rule met in {hv['pairs_meeting_the_retirement_rule']} of "
      f"{hv['consecutive_pairs']} pairs; today {today['verdict']!r} (rests on {today['rests_on_channel']}); "
      f"{ {k: v for k, v in rules.items() if not v} or 'rules ok'}")

# S18 base rates and the naive forecasts
br = J["base_rates"]
cf_ok = all(m["carry_forward"].get("E_expected_from_persistence") is None or m["base_rates"]["carryover_slope"] is None
            or abs(m["carry_forward"]["E_expected_from_persistence"]
                   - (m["base_rates"]["carryover_intercept"] + m["base_rates"]["carryover_slope"] * m["latest"]["E_signed"])) < 1e-12
            for m in J["measures"])
p_ok = all(m["carry_forward"].get("p_same_zone_from_persistence") is None or 0 <= m["carry_forward"]["p_same_zone_from_persistence"] <= 1
           for m in J["measures"])
check("S18 base rates: pooled over the ten counted measures with E (not 4, whose history is its own, nor 2), a visible excess "
      "(|E| >= 1) continued with the same sign in 50-70% of 1990-2019 cases and stayed beyond 1 far less often; each "
      "measure's persistence forecast is its carry-over regression at today's E, with the chance that persistence alone "
      "gives today's reading",
      0.5 <= br["pooled_p_continue_when_visible"] <= 0.7 and br["pooled_p_stays_clear_when_visible"] < br["pooled_p_continue_when_visible"]
      and br["n_visible_windows"] > 200 and cf_ok and p_ok and 4 not in br["pooled_over"] and 2 not in br["pooled_over"],
      f"continue {br['pooled_p_continue_when_visible']:.3f}, stays clear {br['pooled_p_stays_clear_when_visible']:.3f}, "
      f"n {br['n_visible_windows']}; measure 2 stays above its 95th percentile {br['dispersion_p_stays_above_p95']}")

# S19 vintages
vbad = []
for sid in S.MANIFEST:
    v = J["vintages"].get(sid)
    h = S._sha(open(os.path.join(S.CACHE, sid + ".csv")).read())
    if v is None or v["sha256"] != h or v["last"] != str(cached(sid).index[-1].date()):
        vbad.append(sid)
check("S19 every series' vintage (download date, SHA-256, first and last observation) is in the results and matches the "
      "cached file, so revisions are visible", not vbad, f"mismatches {vbad}" if vbad else f"{len(J['vintages'])} vintages")

# S20 the next release, past a month never published: October 2025 (the shutdown) has no household survey or CPI, so the
# 12-month change ending October 2026 has no starting point. A run with a synthetic October 2026 must still complete.
EXT = {"LNS14027662", "LNS14027660", "UNRATE", "CPIAUCSL", "CUSR0000SEHF01", "SAHMREALTIME"}


def extended(sid):
    s_ = ALL[sid]
    s_ = s_[s_.index <= pd.Timestamp("2026-09-30")]   # as of the October 2026 release, whatever the cache's vintage
    if sid in EXT:
        more = pd.date_range(s_.index[-1] + pd.DateOffset(months=1), "2026-10-01", freq="MS")
        s_ = pd.concat([s_, pd.Series(s_.iloc[-1], more)])
    return s_


tmp2 = tempfile.mkdtemp(prefix="splits_check_")
saved = {k: getattr(S, k) for k in SAVED_ATTRS}
err = None
try:
    S.VINTAGES, S.RESULTS = os.path.join(tmp2, "v.json"), os.path.join(tmp2, "r.json")
    S.BASELINE, S.FIGURE = os.path.join(tmp2, "b.json"), os.path.join(tmp2, "f.png")
    S.fred_titles = lambda refresh=False: {}
    S.fetch = lambda sid, refresh=False, vint=None: extended(sid)
    S._git = lambda *a: None
    R2 = run_main([], dt.date(2026, 11, 8))
except Exception as e:  # noqa: BLE001
    err, R2 = repr(e), None
finally:
    for k, v in saved.items():
        setattr(S, k, v)
if R2:
    g3 = next(m for m in R2["measures"] if m["key"] == "graduates")
    el = next(w for w in R2["watch"] if w["key"] == "electricity")
    h5 = next(m for m in R2["measures"] if m["key"] == "hiring")
check("S20 a release past a month never published completes: with a synthetic October 2026, measure 3 reads the window "
      "ending October 2026 (its October 2025 starting point is the 3-month average of August and September), the electricity "
      "watch item reports October 2026 with no 12-month change rather than failing, and measure 5 keeps its last full window",
      err is None and R2 is not None and g3["latest"]["date"] == "2026-10-01" and el["date"] == "2026-10" and el["change_12m"] is None
      and h5["latest"]["date"] <= "2026-09-01",
      err or f"graduates {g3['latest']['date']} E {g3['latest']['E_signed']:+.2f}; electricity {el['date']} change {el['change_12m']}; "
             f"hiring {h5['latest']['date']}")

# S21 what had been seen before the freeze is named in the baseline; the wealth context is computed, not typed
w = J["context"]["wealth"]
t1 = ALL["WFRBST01134"]
check("S21 the baseline names every series published after the 2026-10-13 vintage (seen before the freeze); the wealth "
      "shares on the website come from the Fed's distributional accounts, with the top 1%'s series high and the top 10%'s "
      "peak computed",
      set(S.SEEN_BY_2026_10_13) == set(S.MANIFEST) and isinstance(BL.get("published_after_the_2026_10_13_vintage"), list)
      and BL["published_after_the_2026_10_13_vintage"] == []
      and abs(w["top1_pct"] - float(t1.iloc[-1])) < 1e-9 and w["top1_is_series_high"] == bool(t1.iloc[-1] > t1.iloc[:-1].max()),
      f"top 1% {w['top1_pct']}% ({w['date']}; series high {w['top1_is_series_high']}), top 10% {w['top10_pct']:.1f}% "
      f"(peak {w['top10_peak']})")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
