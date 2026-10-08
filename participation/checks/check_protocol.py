# check_protocol.py — the pipeline (code/build.py, code/specs.py, code/confirm.py) against PROTOCOL.md sections 3 and 5.
#   (a) the data manifest: data/manifest.json is the one the code writes; every query pins every dimension but freq and
#       geo; the datasets and codes match a transcription of the protocol; every test's variables come from it and
#       every query serves a test;
#   (b) each test's outcome, regressor, other terms, controls, years, sign, inference and fixed effects match a table
#       transcribed from PROTOCOL.md section 5 (PROTOCOL_TESTS below: compare it with the protocol line by line), as do
#       the families, the secondaries (their whole equation: base terms, added terms and controls) and the robustness
#       table, and the sample exclusions;
#   (c) the variables, recomputed here by hand from a synthetic world's raw frames (bands, C7's unemployment, q and its
#       lag and lead, C4's blanking of u and c cells);
#   (d) C2: 2020 and 2021 dropped; (e) C1: the UK capped at 2019; (f) C3: break lists and dummies; (g) C9: F_c from the
#       first three available years within 2003-2008, standardised;
#   (h) the verdict rules of section 5 (Holm, contradicted, the leave-one-out qualifier, the intersection-union C-3,
#       the model-level verdict) on constructed p-values; verdict_eligible only on primary tests;
#   (i) the synthetic end-to-end run (results/simulate_pipeline.json from code/simulate_pipeline.py): planted effects
#       recovered, nulls rejected at about the nominal rate, labels and model verdicts as section 5 says;
#   (j) confirm.py refuses without the E-freeze tag (real git state), with a committed confirm result, without a
#       committed explore-half result, and runs end to end on synthetic data when the (simulated) tags allow it: the
#       frozen split, the MDE report (explore half and projected), and the bug-policy fallback for a deviated test.
# The network is blocked for the whole run.
#
# Run from participation/:  ../venv/Scripts/python.exe checks/check_protocol.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import inspect
import json
import math
import os
import shutil
import socket
import sys
import tempfile

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import eurostat as es  # noqa: E402
import requests  # noqa: E402
import build  # noqa: E402
import inference as inf  # noqa: E402
import specs  # noqa: E402
import confirm  # noqa: E402
import simulate_pipeline as sim  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


NET = []


def _blocked(*a, **k):
    NET.append(1)
    raise ConnectionError("network blocked by check_protocol")


requests.adapters.HTTPAdapter.send = _blocked
socket.create_connection = _blocked
socket.socket.connect = _blocked

# ---------------------------------------------------------------- the transcriptions

AP = ["Y25-29", "Y30-34", "Y35-39", "Y40-44", "Y45-49", "Y50-54"]
# PROTOCOL C5-C9 and section 5, the data each measure is built from: manifest id -> (dataset, {dimension: codes}).
PROTOCOL_DATA = {
    "act": ("lfsa_argan", {"unit": {"PC"}, "sex": {"M", "F"}, "age": set(AP) | {"Y55-59", "Y60-64"},
                           "citizen": {"NAT", "TOTAL"}}),                      # C5: activity, nationals; TOTAL robustness
    "emp": ("lfsa_ergan", {"unit": {"PC"}, "sex": {"M", "F"}, "age": {"Y20-24"} | set(AP),
                           "citizen": {"NAT", "TOTAL"}}),                      # C5: employment (C-4)
    "une": ("une_rt_a", {"unit": {"PC_ACT"}, "sex": {"T"}, "age": {"Y25-74", "Y25-54", "Y15-29"}}),  # C7, C-6, C-1 sec
    "une_lfs": ("lfsa_urgan", {"unit": {"PC"}, "sex": {"T"}, "age": {"Y25-74", "Y25-54", "Y15-29"},
                               "citizen": {"TOTAL"}}),                         # C7: 'or failing that lfsa_urgan'
    "hicp": ("prc_hicp_aind", {"unit": {"INX_A_AVG"}, "coicop": {"CP041", "IGD_NNRG", "CP00"}}),  # C6
    "hpi": ("prc_hpi_a", {"purchase": {"TOTAL"}, "unit": {"I15_A_AVG", "I25_A_AVG"}}),  # C6 robustness
    "hpi_el": ("tipsho20", {"unit": {"I15_A_AVG"}}),                           # C6: tipsho20 for Greece
    "comp": ("nama_10_lp_ulc", {"na_item": {"D1_SAL_PER"}, "unit": {"NAC"}}),  # C6: national currency
    "cores": ("ilc_lvps08", {"age": {"Y25-34"}, "sex": {"T"}, "unit": {"PC"}}),  # C9, C-1
    "tenure": ("ilc_lvps05", {"tenure": {"OWN_NL"}, "sex": {"T"}, "age": {"Y55-64"}, "unit": {"PC"}}),  # C-1 sec
    "stud": ("ilc_lvps09", {"wstatus": {"EDUC"}, "age": {"Y18-24"}, "unit": {"PC"}}),  # C-6 secondary
    "educ": ("edat_lfse_19", {"sex": {"T"}, "age": {"Y20-24"}, "wstatus": {"POP"}, "training": {"FE"},
                              "unit": {"PC"}}),                                # C-6
    "occ": ("lfsa_egais", {"unit": {"THS_PER"}, "sex": {"T"}, "age": {"Y15-24", "Y15-64"}, "wstatus": {"EMP"},
                           "isco08": {"OC4", "OC7", "OC8", "TOTAL"}}),         # C-4 (group 4 at 15-24), C-5 (4, 7, 8)
    "pop": ("demo_pjan", {"unit": {"NR"}, "sex": {"T"}, "age": {f"Y{a}" for a in range(13, 100)} | {"Y_OPEN"}}),  # C-5
}
LQ, SILC_Y, C4Y = (1997, 2025), (2005, 2025), [2016, 2017, 2018, 2019, 2022, 2023, 2024, 2025]
# PROTOCOL section 5, test by test. Q = log q_{c,t-1} (C6); F = F_c (C9); U = U_ct (C7).
# id: (family, outcome [(sign, variable)], tested term, other terms, controls, years, H1 side, inference, fixed effects)
PROTOCOL_TESTS = {
    # D1: A_ct = a_c + d_t + b1 log q_{c,t-1} + b2 (log q_{c,t-1} x F_c) + g U_ct + breaks; A = activity 25-34; b2 < 0
    "D1": ("D", [(1, "A2534")], "Q*F", ["Q"], ["U"], LQ, -1, "wcr", ["geo", "year"]),
    # D2: the same outcome on log q_{c,t-1} and (log q_{c,t-1} - m_c)^2; the square < 0
    "D2": ("D", [(1, "A2534")], "sqdev(Q)", ["Q"], ["U"], LQ, -1, "wcr", ["geo", "year"]),
    # C-1: ilc_lvps08 25-34 (sex T) on log q_{c,t-1}; years 2005-2025; b > 0 (U_ct: section 5's default)
    "C1": ("C", [(1, "coresid2534")], "Q", [], ["U"], SILC_Y, 1, "wcr", ["geo", "year"]),
    # C-2: A(25-34) - A(55-64) on log q_{c,t-1}; b > 0
    "C2": ("C", [(1, "A2534"), (-1, "A5564")], "Q", [], ["U"], LQ, 1, "wcr", ["geo", "year"]),
    # C-3 leg 1: A_W(25-54) - A_M(25-54) on log q_{c,t-1}, H1 > 0
    "C3a": ("C", [(1, "AW2554"), (-1, "AM2554")], "Q", [], ["U"], LQ, 1, "wcr", ["geo", "year"]),
    # C-3 leg 2: A_W(25-54) on log q_{c,t-1}, H1 > 0
    "C3b": ("C", [(1, "AW2554")], "Q", [], ["U"], LQ, 1, "wcr", ["geo", "year"]),
    # C-4: E(20-24) - E(25-54) on X_c x 1[year >= 2023], years 2016-2019 and 2022-2025; b < 0; RI primary (CR1)
    "C4": ("C", [(1, "E2024"), (-1, "E2554")], "X*post2023", [], ["U"], C4Y, -1, "ri", ["geo", "year"]),
    # C-5: change in groups 4, 7, 8 share 2011-2019 on predicted aging; stratum FE only; b < 0; RI (HC2)
    "C5": ("C", [(1, "routine_change")], "aging_pred", [], [], (2011, 2019), -1, "ri", ["stratum"]),
    # C-6: 'the share of 20-24-year-olds in formal education (edat_lfse_19, wstatus POP, training FE) on U(25-54),
    # within the LFS window'; 'Controls: none beyond the fixed effects and breaks'; H1 b > 0.
    "C6": ("C", [(1, "educ2024")], "U2554", [], [], LQ, 1, "wcr", ["geo", "year"]),
}
# Readings the protocol's first wording left open were settled in PROTOCOL.md itself before the freeze (2026-10-08):
# C3 from control series too, C5's sex rule, C7's per-country fallback, C-4 without the UK, C-5's breaks, C-6's
# controls and window, D1's top quartile, the robustness table, Holm over the whole family, the leave-one-out
# qualifier in place of a G* threshold.
PROTOCOL_EXCLUDE = {"C4": ["UK"]}                 # C-4 'Sample: the UK is excluded'
PROTOCOL_STUDENTIZE = {"C4": "CR1", "C5": "HC2"}
PROTOCOL_FAMILIES = {"D": ["D1", "D2"], "C": ["C1", "C2", "C3", "C4", "C5", "C6"]}
# Secondaries, no verdict: id -> (base, tested term, other terms, side (0 when no sign is registered), controls). Each
# is its base equation plus the stated terms: the merged equation's regressors are the base's, re-ordered, plus these.
PROTOCOL_SECONDARY = {
    # D1: the implied slope b1 + b2 F at the top-quartile F: Q with Q x (F - F75) (the same equation, reparametrised)
    "D1.slope_top_quartile": ("D1", "Q", ["Q*(F-F75)"], 0, ["U"]),
    # C-1: 'with youth unemployment at 15-29 added'
    "C1.youth_unemployment": ("C1", "Q", [], 1, ["U", "U1529"]),
    # C-1: 'interacted with the 55-64 outright-owner share' (no sign given)
    "C1.outright_owners": ("C1", "Q*O", ["Q"], 0, ["U"]),
    # C-6: the C-6 equation (on U 25-54) plus 'log q x (1 - share of students 18-24 living with their parents)', < 0
    "C6.student_independence": ("C6", "Q*I", ["Q", "U2554"], -1, []),
}
# Robustness, no verdicts: section 5's table, run -> the tests it applies to (C-3 = both legs).
PROTOCOL_ROBUSTNESS = {
    "all_residents": {"D1", "D2", "C2", "C3a", "C3b", "C4"},   # LFS rates by citizenship
    "q_hpi": {"D1", "D2", "C1", "C2", "C3a", "C3b"},           # the alternative q measures of C6
    "q_cp00": {"D1", "D2", "C1", "C2", "C3a", "C3b"},
    "q_comp": {"D1", "D2", "C1", "C2", "C3a", "C3b"},
    "country_trends": {"D1", "D2", "C1", "C2", "C3a", "C3b", "C4", "C6"},
    "long_differences": {"D1", "D2", "C1", "C2", "C3a", "C3b", "C6"},
    "excl_2008_2013": {"D1", "D2", "C1", "C2", "C3a", "C3b", "C6"},
    "lead": {"D1", "D2", "C1", "C2", "C3a", "C3b"},
    "drop_routine_breaks": {"C5"},
}

# ---------------------------------------------------------------- (a) the manifest

print("(a) the data manifest")
disk = json.load(open(build.MANIFEST_PATH, encoding="utf-8"))
mine = json.loads(json.dumps(build.manifest()))
check("A1 data/manifest.json is the manifest the code writes (queries and variable map)",
      disk["entries"] == mine["entries"] and disk["variables"] == mine["variables"]
      and disk["country_level"] == mine["country_level"], f"{len(disk['entries'])} queries")
bad = [m["id"] for m in build.MANIFEST if set(m["filters"]) != set(m["dimensions"]) - {"freq", "geo"}]
check("A2 every query pins every dimension but freq and geo (the response cannot hold unintended cells)", not bad,
      f"not pinned: {bad}" if bad else "")


def as_sets(f):
    return {k: ({v} if isinstance(v, str) else set(v)) for k, v in f.items()}


diff = [m["id"] for m in build.MANIFEST
        if m["id"] not in PROTOCOL_DATA or PROTOCOL_DATA[m["id"]] != (m["dataset"], as_sets(m["filters"]))]
check("A3 datasets and codes match the protocol's (C5-C9, section 5)",
      not diff and set(PROTOCOL_DATA) == set(build.BY_ID), f"differ: {diff}" if diff else
      f"{len(PROTOCOL_DATA)} queries")
check("A4 the countries left out of a query are those the SDMX geo codelists lack (une_rt_a: UK; prc_hpi_a: EL), "
      "and tipsho20 serves Greece only",
      {m["id"]: m.get("absent", []) for m in build.MANIFEST if m.get("absent")} == {"une": ["UK"], "hpi": ["EL"]}
      and build.BY_ID["hpi_el"].get("only") == ["EL"] and build.BY_ID["pop"].get("since") == 2011)

LEVEL_OF = {"F": "F_raw", "O": "owner_outright_5564", "I": "student_indep", "X": "X_c"}


def uses(spec, variant=None):
    q = specs.Q_ALT.get(variant, "logq_l1")
    v = {(o + "_all" if variant == "all_residents" else o) for _, o in spec["outcome"]} | set(spec["controls"])
    for t in [spec["x"]] + list(spec["z"]):
        cols, lv = specs._term_needs(t, q)
        v |= set(cols) | {LEVEL_OF[x] for x in lv}
    if variant == "lead":
        v.add("logq_f1")
    return v


all_specs = [(k, s, None) for k, s in specs.TESTS.items()]
all_specs += [(k, specs._merge(specs.TESTS[s["base"]], s), None) for k, s in specs.SECONDARY.items()]
all_specs += [(f"{t}.{v}", specs.TESTS[t], v) for v, ts in specs.ROBUSTNESS.items() for t in ts]
src = {**{k: v[0] for k, v in build.VARIABLES.items()}, **{k: v[0] for k, v in build.LEVEL.items()}}
missing, used_ids = {}, set()
for k, s, v in all_specs:
    u = uses(s, v)
    if "aging_pred" in u or s.get("cross_section"):
        u |= {"aging_pred", "routine_change"}
    unk = sorted(x for x in u if x not in src)
    if unk:
        missing[k] = unk
    for x in u:
        used_ids.update(src.get(x, []))
check("A5 every test, secondary and robustness variant uses only manifest variables, and every query serves one",
      not missing and used_ids == set(build.BY_ID),
      f"unknown {missing}; unused queries {sorted(set(build.BY_ID) - used_ids)}" if missing or used_ids != set(build.BY_ID)
      else f"{len(all_specs)} specifications over {len(used_ids)} queries")

# ---------------------------------------------------------------- (b) the specifications

print("(b) the specifications against PROTOCOL.md section 5")
rows = []
for k, (fam, out, x, z, ctrl, yrs, side, infer, fe) in PROTOCOL_TESTS.items():
    s = specs.TESTS.get(k, {})
    got = (s.get("family"), s.get("outcome"), s.get("x"), s.get("z"), s.get("controls"), s.get("years"),
           s.get("side"), s.get("inference"), s.get("fe"))
    want = (fam, out, x, z, ctrl, yrs, side, infer, fe)
    rows.append((k, got == want, [n for n, a, b in zip(("family", "outcome", "x", "z", "controls", "years", "side",
                                                         "inference", "fe"), got, want) if a != b]))
for k, ok, d in rows:
    check(f"B1 {k}: family, outcome, regressor, other terms, controls, years, sign, inference, fixed effects", ok,
          f"differs in {d}" if d else f"{specs.TESTS[k]['what']}")
check("B2 no test beyond the protocol's; C-4 studentises CR1 and C-5 HC2; C-5 is a cross-section",
      set(specs.TESTS) == set(PROTOCOL_TESTS) and all(specs.TESTS[k]["studentize"] == v
                                                     for k, v in PROTOCOL_STUDENTIZE.items())
      and specs.TESTS["C5"].get("cross_section") and specs.FAMILIES == PROTOCOL_FAMILIES
      and specs.PRIMARY == ["D1", "D2", "C1", "C2", "C3", "C4", "C5", "C6"])
sec_bad = []
for k, (b, x, z, sd, c) in PROTOCOL_SECONDARY.items():
    m = specs._merge(specs.TESTS[b], specs.SECONDARY.get(k, {"base": b}))
    base_terms = {specs.TESTS[b]["x"], *specs.TESTS[b]["z"], *specs.TESTS[b]["controls"]}
    got_terms = {m["x"], *m["z"], *m["controls"]}
    if (specs.SECONDARY.get(k, {}).get("base") != b or (m["x"], list(m["z"]), m["side"], list(m["controls"]))
            != (x, z, sd, c) or m["outcome"] != specs.TESTS[b]["outcome"]
            or not (base_terms - {"Q*F"} <= got_terms or k == "D1.slope_top_quartile")):
        sec_bad.append(k)
check("B3 the secondaries, whole equations (D1 top-quartile slope, C-1 with youth unemployment and x outright owners, "
      "C-6 x student independence < 0 inside the C-6 equation) and C-4's pre-trend event study",
      set(specs.SECONDARY) == set(PROTOCOL_SECONDARY) and not sec_bad and callable(specs.event_study),
      f"differ: {sec_bad}" if sec_bad else "")
check("B4 the robustness table (all residents, the three alternative q, country trends, five-year long differences, "
      "excluding 2008-2013, the lead, C-5 without break countries), each where section 5 applies it, none with a "
      "verdict",
      {k: set(v) for k, v in specs.ROBUSTNESS.items()} == PROTOCOL_ROBUSTNESS
      and specs.Q_ALT == {"q_hpi": "logq_hpi_l1", "q_cp00": "logq_cp00_l1", "q_comp": "logq_comp_l1"})
check("B7 sample exclusions: C-4 without the UK, no other test excludes a country",
      {k: s["exclude"] for k, s in specs.TESTS.items() if s.get("exclude")} == PROTOCOL_EXCLUDE)
check("B6 specs.DEVIATED (section 7's fallback list) is empty before the E freeze and within the primary tests",
      specs.DEVIATED == frozenset() and specs.DEVIATED <= set(specs.PRIMARY))
sig = inspect.signature(specs.run).parameters
check("B5 production inference: B = R = 9999 by default, Webb six-point weights, leave-one-out threshold 0.10 and "
      "on by default, Holm at 0.05",
      sig["B"].default == 9999 and sig["R"].default == 9999 and specs.LOO_P == 0.10 and sig["loo"].default is True
      and specs.ALPHA == 0.05
      and np.allclose(sorted(inf.WEBB), sorted([-math.sqrt(1.5), -1, -math.sqrt(.5), math.sqrt(.5), 1, math.sqrt(1.5)])))

# ---------------------------------------------------------------- (c) the variables, by hand

print("(c) the variables, recomputed by hand from a synthetic world")
W = sim.World(4242, sim.PLANT, sim.C)
cy, cl, _ = sim.with_world(W, "confirm")
fr = W.frames


def hand_cells(df, **sel):
    d = df
    for k, v in sel.items():
        d = d[d[k] == v]
    v = d["value"].where(~d["flag"].str.contains("u|c", regex=True))
    return pd.Series(v.to_numpy(float), index=pd.MultiIndex.from_arrays([d["geo"], d["year"]]))


def hand_band(df, cells):
    return pd.concat([hand_cells(df, **c) for c in cells], axis=1).mean(axis=1, skipna=False)


def same(a, b):
    a, b = a.align(b, join="inner")
    x, y = a.to_numpy(float), b.to_numpy(float)
    return bool(len(x)) and bool(np.all((np.isnan(x) & np.isnan(y)) | (np.abs(x - y) <= 1e-9)))


def cmp(name, series):
    s = cy[name]
    return same(s, series.reindex(s.index))


hand = {}
for suf, cz in (("", "NAT"), ("_all", "TOTAL")):
    hand["A2534" + suf] = hand_band(fr["act"], [dict(sex=s, age=a, citizen=cz) for s in "MF" for a in AP[:2]])
    hand["A5564" + suf] = hand_band(fr["act"], [dict(sex=s, age=a, citizen=cz) for s in "MF" for a in ("Y55-59", "Y60-64")])
    hand["AW2554" + suf] = hand_band(fr["act"], [dict(sex="F", age=a, citizen=cz) for a in AP])
    hand["AM2554" + suf] = hand_band(fr["act"], [dict(sex="M", age=a, citizen=cz) for a in AP])
    hand["E2024" + suf] = hand_band(fr["emp"], [dict(sex=s, age="Y20-24", citizen=cz) for s in "MF"])
    hand["E2554" + suf] = hand_band(fr["emp"], [dict(sex=s, age=a, citizen=cz) for s in "MF" for a in AP])
bad = [k for k, v in hand.items() if not cmp(k, v)]
check("C1 bands (C5): equal-weight means of the five-year M/F cells, nationals and all residents, missing if a cell "
      "is", not bad, f"differ: {bad}" if bad else f"{len(hand)} variables")
une, urg = fr["une"], fr["une_lfs"]
hu = pd.concat([hand_cells(une[une["geo"] == g], age="Y25-74") if g in set(une["geo"])
                else hand_cells(urg[urg["geo"] == g], age="Y25-74") for g in sim.C])
check("C2 U (C7): une_rt_a Y25-74 PC_ACT for every country it covers, lfsa_urgan Y25-74 TOTAL for the UK",
      cmp("U", hu) and "UK" not in set(une["geo"]) and np.isfinite(cy.loc["UK", "U"]).any())
cp = hand_cells(fr["hicp"], coicop="CP041")
nn = hand_cells(fr["hicp"], coicop="IGD_NNRG")
lq = np.log(cp) - np.log(nn.reindex(cp.index))
lag = pd.Series(lq.to_numpy(), index=pd.MultiIndex.from_arrays([lq.index.get_level_values(0),
                                                               lq.index.get_level_values(1) + 1]))
lead = pd.Series(lq.to_numpy(), index=pd.MultiIndex.from_arrays([lq.index.get_level_values(0),
                                                                lq.index.get_level_values(1) - 1]))
check("C3 q (C6): log(CP041 / IGD_NNRG), INX_A_AVG; logq_l1 is year t-1's, logq_f1 year t+1's",
      cmp("logq", lq) and cmp("logq_l1", lag) and cmp("logq_f1", lead))
act = fr["act"]
flagged = act[act["flag"].str.contains("u|c", regex=True) & act["value"].notna() & (act["citizen"] == "NAT")
              & act["age"].isin(AP[:2]) & ~act["year"].isin([2020, 2021]) & ~((act["geo"] == "UK") & (act["year"] > 2019))]
blank = all(np.isnan(cy.loc[(g, y), "A2534"]) for g, y in zip(flagged["geo"], flagged["year"]))
check("C4 C4: cells flagged u or c are missing (their values are in the raw frame; the band built on them is missing)",
      len(flagged) > 0 and blank, f"{len(flagged)} flagged cells with values, all blanked")

# ---------------------------------------------------------------- (d), (e) years and the UK

print("(d) C2: 2020 and 2021; (e) C1: the UK")
ctx = specs.Ctx(cl, specs.f_constants(cl, sim.C))
frames = {k: specs.frame(cy, s, ctx, sim.C) for k, s in specs.TESTS.items() if not s.get("cross_section")}
frames.update({f"{t}.{v}": specs.frame(cy, specs.TESTS[t], ctx, sim.C, v) for v, ts in specs.ROBUSTNESS.items()
               for t in ts if not specs.TESTS[t].get("cross_section")})
yrs = set(cy.index.get_level_values(1))
check("D1 2020 and 2021 are not in the panel, nor in any test's or robustness variant's rows",
      not ({2020, 2021} & yrs) and all(not ({2020, 2021} & set(f["M"]["year"])) for f in frames.values()),
      f"{len(frames)} estimation frames")
spans = {k: (int(f["M"]["year"].min()), int(f["M"]["year"].max())) for k, f in frames.items() if "." not in k}
inside = all(PROTOCOL_TESTS[k][5][0] <= lo and hi <= PROTOCOL_TESTS[k][5][1] if isinstance(PROTOCOL_TESTS[k][5], tuple)
             else set(frames[k]["M"]["year"]) <= set(PROTOCOL_TESTS[k][5]) for k, (lo, hi) in spans.items())
check("D2 each test's rows lie inside its window (LFS with q 1997-2025, SILC 2005-2025, C-4 2016-19 and 2022-25)",
      inside and set(frames["C4"]["M"]["year"]) == set(C4Y), str(spans))
ex = frames["D1.excl_2008_2013"]["M"]["year"]
check("D3 the 2008-2013 exclusion drops exactly those years", not (set(range(2008, 2014)) & set(ex))
      and set(frames["D1"]["M"]["year"]) - set(ex) == set(range(2008, 2014)))
uk_raw = ((act["geo"] == "UK") & (act["year"] > 2019) & act["value"].notna()).sum()
uk_rows = [k for k, f in frames.items() if ((f["M"]["geo"] == "UK") & (f["M"]["year"] > 2019)).any()]
raw_uk = {k: v.copy() for k, v in fr.items()}
h = raw_uk["hicp"]
uk20 = h[(h["geo"] == "UK") & (h["year"] == 2019)].copy()
uk20["year"], uk20["value"], uk20["flag"] = 2020, uk20["value"] * 1.5, "b"
raw_uk["hicp"] = pd.concat([h, uk20], ignore_index=True)
cy_uk = build.country_year("confirm", raw=raw_uk, geos=sim.C)
lead_ok = (np.isnan(cy_uk.loc[("UK", 2019), "logq_f1"]) and 2019 not in cy_uk.loc[("UK", 2019), "logq_f1__breaks"]
           and np.isfinite(cy_uk.loc[("UK", 2019), "logq"]))
check("E1 the UK is capped at 2019: its 2020-2025 values in the raw frame reach neither the panel nor any test, nor "
      "the UK's 2019 lead (a planted UK 2020 HICP value and its break flag leave logq_f1 at 2019 missing)",
      uk_raw > 0 and int(cy.xs("UK", level=0).index.max()) <= 2019 and not uk_rows and lead_ok,
      f"{uk_raw} raw UK cells after 2019 dropped")

# ---------------------------------------------------------------- (f) C3 breaks

print("(f) C3: break dummies")


def hand_breaks(df, cells):
    out = {}
    for c in cells:
        d = df
        for k, v in c.items():
            d = d[d[k] == v]
        for g, y in zip(d.loc[d["flag"].str.contains("b"), "geo"], d.loc[d["flag"].str.contains("b"), "year"]):
            if not (g == "UK" and y > 2019):          # C1: the UK's cells after 2019 are gone before anything is built
                out.setdefault(g, set()).add(int(y))
    return out


def lists(name):
    return {g: set(v) for g, v in cy[name + "__breaks"].groupby(level=0).first().items() if v}


hb_a = hand_breaks(act, [dict(sex=s, age=a, citizen="NAT") for s in "MF" for a in AP[:2]])
hb_q = hand_breaks(fr["hicp"], [dict(coicop="CP041"), dict(coicop="IGD_NNRG")])
hb_u = {g: v for g, v in hand_breaks(une, [dict(age="Y25-74")]).items()}
hb_u.update(hand_breaks(urg[urg["geo"] == "UK"], [dict(age="Y25-74")]))
check("F1 break lists: every 'b' flag of any cell of the variable, per country (A2534, U), and for the lagged q the "
      "year after the flag, for the lead the year before",
      lists("A2534") == hb_a and lists("U") == hb_u and hb_q
      and lists("logq_l1") == {g: {y + 1 for y in v} for g, v in hb_q.items()}
      and lists("logq_f1") == {g: {y - 1 for y in v} for g, v in hb_q.items()},
      f"A2534 {sum(map(len, hb_a.values()))}, U {sum(map(len, hb_u.values()))}, q {sum(map(len, hb_q.values()))} "
      "break years")
f1 = frames["D1"]
M = f1["M"]
D = specs.break_dummies(M, f1["breaks"])
want = set()
for g, t in set().union(*[{(g, y) for g, ys in lists(v).items() for y in ys} for v in ("A2534", "logq_l1", "U")]):
    m = (M["geo"] == g).to_numpy()
    col = (m & (M["year"].to_numpy() >= t)).astype(float)
    if m.any() and col[m].min() != col[m].max():
        want.add(col.tobytes())
got = {D[:, j].tobytes() for j in range(D.shape[1])}
check("F2 D1's dummies are exactly the distinct 1[geo = c, year >= tau] over the breaks of its outcome, regressor and "
      "control that vary within c's rows", got == want and D.shape[1] == len(got), f"{D.shape[1]} dummies")
toy = pd.DataFrame({"geo": ["AT"] * 4, "year": [2004, 2005, 2006, 2007], "value": [1.0, 2.0, 3.0, 4.0],
                    "flag": ["", "bu", "c", "b"]})
v, b = build.cell(toy)
check("F3 a 'bu' cell is a break and missing; a 'c' cell is missing; plain 'b' a break",
      b == {"AT": [2005, 2007]} and np.isnan(v[("AT", 2005)]) and np.isnan(v[("AT", 2006)]) and v[("AT", 2007)] == 4)
ld = specs.long_differences(f1)
check("F4 long differences: five-year differences on the grid 1997-2022, end years only, never 2020 or 2021",
      set(ld[4]["year"]) <= set(specs.LD_GRID[1:]) and not ({2020, 2021} & set(ld[4]["year"])))

# ---------------------------------------------------------------- (g) C9 F_c

print("(g) C9: F_c")
s = pd.Series([50.0, 40.0, np.nan, 30.0, 20.0, 10.0, 5.0], index=[2002, 2004, 2005, 2006, 2007, 2008, 2009])
check("G1 F_c = mean of the first three available years within 2003-2008 (2002 and 2009 ignored, a missing year "
      "skipped); none in the window gives NaN", build.first_three(s) == (30.0, [2004, 2006, 2007])
      and np.isnan(build.first_three(pd.Series([1.0, 2.0], index=[2001, 2010]))[0]))
cf = hand_cells(fr["cores"])
hf = {}
for g in sim.C:
    x = cf.xs(g, level=0) if g in set(cf.index.get_level_values(0)) else pd.Series(dtype=float)
    x = x[(x.index >= 2003) & (x.index <= 2008)].dropna().sort_index()
    hf[g] = float(x.iloc[:3].mean()) if len(x) else np.nan
ok = all((np.isnan(hf[g]) and np.isnan(cl.loc[g, "F_raw"])) or abs(hf[g] - cl.loc[g, "F_raw"]) < 1e-9 for g in sim.C)
nof = [g for g in sim.C if np.isnan(hf[g])]
check("G2 the world's F_raw recomputed by hand from ilc_lvps08 (u and c blanked); countries without one leave D1",
      ok and nof and not (set(nof) & set(frames["D1"]["M"]["geo"])), f"no F: {nof}")
Fz = ctx.F.dropna()
alt = specs.Ctx(cl, (10.0, 2.0)).F
check("G3 F is standardised over the countries with a value (mean 0, sd 1, ddof 0); given constants are used as given",
      abs(Fz.mean()) < 1e-12 and abs(Fz.std(ddof=0) - 1) < 1e-12
      and np.allclose(alt.dropna(), (cl["F_raw"].dropna() - 10) / 2))
r1 = specs.estimate(cy, cl, specs.TESTS["D1"], ctx, sim.C, B=199, with_ci=False)
r2 = specs.estimate(cy, cl, specs.TESTS["D1"], specs.Ctx(cl, (10.0, 2.0)), sim.C, B=199, with_ci=False)
check("G4 D1's t and p do not depend on the standardising constants (only b2's units do)",
      abs(r1["t"] - r2["t"]) < 1e-8 and r1["p"] == r2["p"], f"t {r1['t']:.6f} vs {r2['t']:.6f}")
lvl = cl.loc["DE"]
hx = W.frames["occ"]
xo = hand_cells(hx, age="Y15-24", isco08="OC4").xs("DE", level=0) / hand_cells(hx, age="Y15-24", isco08="TOTAL").xs("DE", level=0)


def aged_ratio_change(n_by_age: dict) -> float:
    """C-5 by hand: move every person eight years on (no migration, no mortality), then the ratio of the 56+ to the
    21-55 after minus before. n_by_age: {age: persons}, 100 standing for 100+."""
    def ratio(d):
        return sum(v for a, v in d.items() if a >= 56) / sum(v for a, v in d.items() if 21 <= a <= 55)
    return ratio({a + 8: v for a, v in n_by_age.items()}) - ratio(n_by_age)


toy_ages = list(range(13, 101))
toys = {"one person per age": {a: 1.0 for a in toy_ages},
        "a bulge at 40-50": {a: (5.0 if 40 <= a <= 50 else 1.0) for a in toy_ages},
        "falling with age": {a: 200.0 - 1.5 * a for a in toy_ages}}
toy_ok = []
for name, n in toys.items():
    pdf = pd.DataFrame({"geo": "XX", "year": 2011, "value": [n[100 if c == "Y_OPEN" else int(c[1:])] for c in build.AGES_POP],
                        "flag": "", "age": build.AGES_POP, "sex": "T", "unit": "NR"})
    toy_ok.append(abs(build.aging(pdf, "XX") - aged_ratio_change(n)) < 1e-12)
check("G5 X_c = 100 x OC4 / TOTAL at 15-24, mean of 2018-2019; aging_pred equals the ratio change of three toy "
      "populations aged eight years by hand (one person per age: 8/35); the routine change matches the planted one",
      abs(lvl["X_c"] - 100 * xo.reindex([2018, 2019]).mean()) < 1e-9 and all(toy_ok)
      and abs(aged_ratio_change(toys["one person per age"]) - 8 / 35) < 1e-12
      and np.allclose(cl["routine_change"].reindex(sim.C).to_numpy(float), W.routine_true, atol=1e-6),
      f"toys {toy_ok}")
rb = cl["routine_breaks"]
check("G6 C-5's break years inside 2012-2019 are recorded per country (lfsa_egais 15-64 cells), for the report",
      all(isinstance(v, list) and all(2011 < y <= 2019 for y in v) for v in rb),
      f"{sum(len(v) > 0 for v in rb)} countries with a break in the window")

# ---------------------------------------------------------------- (h) verdict rules

print("(h) the verdict rules")


def r(p, po=None, g=20.0):
    return {"p": p, "p_opposite": 1 - p if po is None else po, "G_star": g}


H = specs.holm
cases = [
    ({"D1": r(0.02), "D2": r(0.03)}, {"D1": "supported", "D2": "supported"}),          # 0.02 <= .025, .03 <= .05
    ({"D1": r(0.03), "D2": r(0.2)}, {"D1": "inconclusive", "D2": "inconclusive"}),     # 0.03 > .025: Holm stops
    ({"D1": r(0.001), "D2": r(0.9, 0.01)}, {"D1": "supported", "D2": "contradicted"}),
    ({"D1": r(0.0001, g=3.0), "D2": r(0.5)}, {"D1": "supported", "D2": "inconclusive"}),       # G* not acted on
    ({"D1": r(0.99, 0.004, g=3.0), "D2": r(0.5)}, {"D1": "contradicted", "D2": "inconclusive"}),
]
c6 = {f"C{i}": r(p) for i, p in zip(range(1, 7), [0.005, 0.009, 0.0125, 0.016, 0.5, 0.6])}
cases.append((c6, {"C1": "supported", "C2": "supported", "C3": "supported", "C4": "supported", "C5": "inconclusive",
                   "C6": "inconclusive"}))         # .005 <= .05/6, .009 <= .05/5, .0125 <= .05/4, .016 <= .05/3, .5 > .05/2
c6b = dict(c6, C3=r(0.013))
cases.append((c6b, {"C1": "supported", "C2": "supported", "C3": "inconclusive", "C4": "inconclusive",
                    "C5": "inconclusive", "C6": "inconclusive"}))
# Holm runs over the whole family: six tests, so C1's p 0.01 faces 0.05/6 and is inconclusive (with five it would
# face 0.01 and be supported).
c6c = {f"C{i}": r(p) for i, p in zip(range(1, 7), [0.01, 0.5, 0.5, 0.5, 0.3, 0.5])}
c6c["C5"] = r(0.3, g=5.0)
cases.append((c6c, {"C1": "inconclusive", "C2": "inconclusive", "C3": "inconclusive", "C4": "inconclusive",
                    "C5": "inconclusive", "C6": "inconclusive"}))
bad = [i for i, (res, want) in enumerate(cases) if H(res) != want]
check("H1 Holm within the whole family: supported, contradicted (Holm on the opposite p), inconclusive; G* not "
      "acted on", not bad,
      f"failing cases {bad}" if bad else f"{len(cases)} cases")
mv = specs.model_verdict
check("H2 the model-level verdict: favours the model (one D supported, none contradicted), against the floor "
      "mechanism (either contradicted), inconclusive otherwise",
      mv({"D1": "supported", "D2": "inconclusive"}) == "favours the model"
      and mv({"D1": "supported", "D2": "contradicted"}) == "against the floor mechanism"
      and mv({"D1": "inconclusive", "D2": "contradicted"}) == "against the floor mechanism"
      and mv({"D1": "inconclusive", "D2": "inconclusive"}) == "inconclusive"
      and mv({"D1": "inconclusive", "D2": "supported"}) == "favours the model")
lo = {"D1": dict(max_p=0.30, max_p_left_out="IS", max_p_opposite=0.9, max_p_opposite_left_out="SE"),
      "D2": dict(max_p=0.04, max_p_left_out="DE", max_p_opposite=0.95, max_p_opposite_left_out="FR"),
      "C1": dict(max_p=0.99, max_p_left_out="ES", max_p_opposite=0.20, max_p_opposite_left_out="IE"),
      "C2": dict(max_p=0.50, max_p_left_out="PT", max_p_opposite=0.50, max_p_opposite_left_out="PT")}
lb = {"D1": "supported", "D2": "supported", "C1": "contradicted", "C2": "inconclusive"}
qu = specs.qualify(lb, lo)
check("H4 the leave-one-out qualifier: a verdict whose own-direction p exceeds 0.10 with one country left out 'rests "
      "on one country (XX)'; none otherwise or for inconclusive tests; the model verdict carries the D qualifiers",
      qu == {"D1": "rests on one country (IS)", "D2": "", "C1": "rests on one country (IE)", "C2": ""}
      and specs.model_qualifier({"D1": "supported", "D2": "supported"}, qu) == "D1: rests on one country (IS)"
      and specs.model_qualifier({"D1": "supported", "D2": "contradicted"}, qu) == ""
      and specs.model_qualifier({"D1": "inconclusive", "D2": "inconclusive"}, qu) == "", str(qu))
iu = specs.intersection(dict(p=0.01, p_opposite=0.99, G_star=12.0, n=100, G=31),
                        dict(p=0.04, p_opposite=0.96, G_star=9.0, n=120, G=31))
check("H3 C-3 intersection-union: p is the larger leg's, G* the smaller", iu["p"] == 0.04 and iu["G_star"] == 9.0
      and iu["p_opposite"] == 0.99)

# ---------------------------------------------------------------- (i) the synthetic end-to-end run

print("(i) the synthetic end-to-end run (results/simulate_pipeline.json)")
S = json.load(open(os.path.join(ROOT, "results", "simulate_pipeline.json"), encoding="utf-8"))
P, N, O = S["full_planted"], S["full_null"], S["full_opposite"]
sides = {k: v[6] for k, v in PROTOCOL_TESTS.items()}
rec = {k: P["tests"][k]["beta"] * sides[k] > 0 and P["tests"][k]["p"] <= 0.05 for k in PROTOCOL_TESTS}
check("I1 planted world (B = 9999): every primary test's estimate has the planted sign with one-sided p <= 0.05, "
      "both C-3 legs included", all(rec.values()),
      "; ".join(f"{k} {P['tests'][k]['beta']:.2f} (planted {S['plant'][S['planted_coefficient'][k]]}) "
                f"p {P['tests'][k]['p']:.4f}" for k in PROTOCOL_TESTS))
ci_ok = [k for k in PROTOCOL_TESTS if P["tests"][k]["ci"]
         and P["tests"][k]["ci"][0] <= S["plant"][S["planted_coefficient"][k]] <= P["tests"][k]["ci"][1]]
check("I2 the planted coefficient lies inside the 95% interval for most tests (omitted-term bias aside: C-2 and C-3 "
      "omit D1's and D2's terms by design)", len(ci_ok) >= 6, f"inside for {ci_ok}")
lab_ok = all(P["verdicts"][k] == "supported" for k in specs.PRIMARY)
gu = P["panel"]["geos_used"]
loo_ok = all(P["leave_one_out"][k]["n_left_out"] == len(gu["C3a" if k == "C3" else k]) for k in specs.PRIMARY)
check("I3 planted world: every primary test supported, the model verdict 'favours the model', and every primary test "
      "rerun once per country it uses (leave one out)", lab_ok and loo_ok and P["model_verdict"] == "favours the model",
      f"{P['verdicts']}; qualifiers {P['qualifiers']}")
check("I4 opposite world (D1's and D2's terms reversed): D1 and D2 contradicted, model 'against the floor mechanism'",
      O["verdicts"]["D1"] == "contradicted" and O["verdicts"]["D2"] == "contradicted"
      and O["model_verdict"] == "against the floor mechanism", f"{O['verdicts']} -> {O['model_verdict']}")
check("I5 null world (B = 9999): both D tests inconclusive", all(N["verdicts"][k] == "inconclusive"
                                                               for k in ("D1", "D2")), str(N["verdicts"]))
check("I13 C-4 runs without the UK, and C-5's break robustness run exists",
      "UK" not in P["panel"]["geos_used"]["C4"] and "UK" in P["panel"]["geos_used"]["C2"]
      and "C5.drop_routine_breaks" in P["robustness"], str(P["panel"]["geos_used"]["C4"]))
RN, RP = S["reps_null"], S["reps_planted"]
ids = list(PROTOCOL_TESTS)
rates = [RN["reject_5pct"][k] for k in ids] + [RN["reject_5pct"][k + "_opposite"] for k in ids]
check(f"I6 {RN['n']} null worlds: the one-sided 5% tests reject in 2-8% of cases pooled over the {len(ids)} tests and "
      "both directions, no single rate above 15%", RN["n"] >= 200 and 0.02 <= float(np.mean(rates)) <= 0.08
      and max(rates) <= 0.15, f"pooled {np.mean(rates):.3f}, max {max(rates):.2f}: "
      + ", ".join(f"{k} {RN['reject_5pct'][k]:.2f}/{RN['reject_5pct'][k + '_opposite']:.2f}" for k in ids))
# Holm caps each direction's familywise rate at 5%, so a false verdict of either kind is at most 10% per family; the
# bound allows 2.4 Monte Carlo standard errors over 200 worlds.
check("I7 null worlds: a family-level false verdict (supported or contradicted) in at most 15% of worlds per family "
      "(nominal at most 10%), the model verdict 'inconclusive' in at least 85%",
      RN["n"] >= 200 and max(RN["family_any_verdict"].values()) <= 0.15
      and RN["model_verdict"].get("inconclusive", 0) >= 0.85,
      f"{RN['family_any_verdict']}, {RN['model_verdict']}")
sup = {k: RP["labels"].get(f"{k}|supported", 0) for k in specs.PRIMARY}
check(f"I8 {RP['n']} planted worlds: each primary test supported in at least 90%, the model "
      "verdict 'favours the model' in at least 90%", RP["n"] >= 40 and min(sup.values()) >= 0.9
      and RP["model_verdict"].get("favours the model", 0) >= 0.9, f"{sup}; {RP['model_verdict']}")
E = S["explore_run"]
check("I9 the explore half: the pipeline runs on the 16 explore countries, every query asks for explore countries only",
      E["query_geos_within_explore"] and E["geos"] == sorted(sim.SPLIT["explore"])
      and E["queries"] == sorted(m["id"] for m in build.MANIFEST if build.query_geos(m, sim.SPLIT["explore"])),
      f"{E['n_queries']} queries (tipsho20 serves Greece, a confirm country, so the explore half skips it)")
check("I10 the full runs made every manifest query once, and nothing else",
      all(S[k]["queries"] == sorted(build.BY_ID) and S[k]["n_queries"] == len(build.MANIFEST)
          for k in ("full_null", "full_planted", "full_opposite")))
yu = [k for k, v in P["panel"]["years_used"].items() if v and {2020, 2021} & set(v)]
check("I11 in the end-to-end runs no test used 2020 or 2021 and the panel's UK ends in 2019 (raw UK data ran to 2025)",
      not yu and P["panel"]["uk_max_year"] <= 2019 and P["panel"]["uk_activity_after_2019_in_raw"])

gb = RP.get("G_star_below_8", {})
check("I12 the replications record how often G* < 8 (reported, not acted on)",
      set(specs.PRIMARY) <= set(gb), "planted worlds, share with G* < 8: "
      + ", ".join(f"{k} {gb[k]:.2f} (mean G* {RP['G_star_mean'][k]:.1f})" for k in specs.PRIMARY if k in gb))

# ---------------------------------------------------------------- (j) confirm.py

print("(j) confirm.py")
TMP = tempfile.mkdtemp(prefix="check_protocol_")
REAL = {"RAW": es.RAW, "LOG": es.LOG, "_git": es._git, "get": es.get}
log_before = open(es.LOG, "rb").read() if os.path.exists(es.LOG) else b""
res_before = sorted(f for f in os.listdir(os.path.join(ROOT, "results")) if f.startswith("confirm_"))
fetched = []
real_fetch = build.fetch
build.fetch = lambda half: fetched.append(half) or real_fetch(half)


def attempt(fn):
    n0 = len(NET)
    try:
        fn()
        return None, "", len(NET) - n0
    except Exception as e:  # noqa: BLE001
        return type(e), str(e), len(NET) - n0


def has_tag(tag):
    return es._git("rev-parse", "-q", "--verify", f"refs/tags/{tag}")[0] == 0


e_tag = has_tag(es.E_FREEZE)
t, msg, n = attempt(confirm.look)
res_after = sorted(f for f in os.listdir(os.path.join(ROOT, "results")) if f.startswith("confirm_"))
log_after = open(es.LOG, "rb").read() if os.path.exists(es.LOG) else b""
check("J1 in the repository's real state (no E-freeze tag) confirm.py refuses: BlindingError before any fetch, no "
      "network call, no result written, the fetch log untouched",
      (not e_tag) and t is es.BlindingError and n == 0 and not fetched and res_after == res_before
      and log_after == log_before, f"{t.__name__ if t else 'no error'}: {msg[:90]}" if not e_tag
      else "the E-freeze tag exists: this check is for the state before it")


SHA = {es.P_FREEZE: "a" * 40, es.E_FREEZE: "b" * 40}


class FakeGit:
    def __init__(self, tags=(es.P_FREEZE, es.E_FREEZE), committed="", status="", explore_committed=True):
        self.tags, self.committed, self.status = set(tags), committed, status
        self.explore_committed = explore_committed

    def __call__(self, *args):
        if args[:3] == ("rev-parse", "-q", "--verify"):
            t = args[3].removeprefix("refs/tags/").removesuffix("^{commit}")
            return (0, SHA[t] + "\n") if t in self.tags else (1, "")
        if args == ("show", f"{SHA[es.P_FREEZE]}:./data/split.json"):
            return 0, json.dumps(sim.SPLIT)
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[0] == "status":
            return 0, self.status
        if args[0] == "diff":
            return 0, ""
        if args == ("ls-files", "--", "results/specs_explore.json"):
            return 0, "results/specs_explore.json\n" if self.explore_committed else ""
        if args[0] == "ls-files":
            return 0, self.committed
        if args == ("rev-parse", "--short", "HEAD"):
            return 0, "abc1234\n"
        if args == ("rev-parse", "HEAD"):
            return 0, "abc1234" + "0" * 33 + "\n"
        if args == ("rev-parse", "HEAD:./code"):
            return 0, "f" * 40 + "\n"
        return 1, ""


es.RAW, es.LOG = os.path.join(TMP, "raw"), os.path.join(TMP, "fetch_log.jsonl")
confirm.RESULTS = os.path.join(TMP, "results")
os.makedirs(confirm.RESULTS, exist_ok=True)
We = sim.World(77, sim.PLANT, sim.SPLIT["explore"])           # the explore-half run whose MDEs the look carries
cye, cle, _ = sim.with_world(We, "explore")
explore_res = specs.run("explore", cye, cle, B=199, R=199, with_ci=False, secondary=False, robustness=False)
with open(os.path.join(confirm.RESULTS, "specs_explore.json"), "w", encoding="utf-8") as f:
    json.dump(specs.clean_json(explore_res), f)
fetched.clear()
outcomes = {}
for name, g in {"a committed results/confirm_*.json": FakeGit(committed="results/confirm_0123abc.json\n"),
                "only the P-freeze tag": FakeGit(tags=(es.P_FREEZE,)),
                "only the E-freeze tag": FakeGit(tags=(es.E_FREEZE,)),
                "results/specs_explore.json not committed": FakeGit(explore_committed=False),
                "a modified spec": FakeGit(status=" M participation/code/specs.py\n")}.items():
    es._git = g
    t, msg, n = attempt(confirm.look)
    outcomes[name] = (t is es.BlindingError and n == 0, msg[:70])
check("J2 with the tags simulated, confirm.py still refuses: " + ", ".join(outcomes) + "; nothing fetched",
      all(ok for ok, _ in outcomes.values()) and not fetched,
      "; ".join(f"{k}: {m}" for k, (ok, m) in outcomes.items() if not ok))
src_c = inspect.getsource(confirm.look)
check("J3 confirm.look guards first: eurostat.guard('confirm') and the committed-result check come before the fetch",
      src_c.index('es.guard("confirm")') < src_c.index("committed_results()") < src_c.index("build.fetch("))
# a synthetic look: tags simulated, the loader answered by a synthetic world, results to a temporary folder
es._git = FakeGit()
Wc = sim.World(99, sim.PLANT, sim.C)
es.get = sim.Fake(Wc)
build.reset()
t, msg, n = attempt(lambda: outcomes.setdefault("look", confirm.look()))
look = outcomes.get("look")
ok = t is None and look is not None and os.path.exists(os.path.join(TMP, "results", "confirm_abc1234.json"))
if ok:
    full, rep, prim = look["P_full_sample"], look["P_confirm_half_replication"], look["primary"]
    ok = (full["geos"] == sorted(es.COUNTRIES) and rep["geos"] == sorted(sim.SPLIT["confirm"])
          and full["F_standardisation"]["mean"] == rep["F_standardisation"]["mean"]
          and "verdicts" in full and "labels_for_information" in rep and look["E_confirm_half"] is None
          and prim["verdicts"] == full["verdicts"] and prim["full_sample_exploratory"] == []
          and all(v == "full sample" for v in prim["source"].values())
          and all(v == {"explore_cache": "absent"} for v in look["vintage_vs_explore"].values()))
check("J4 a synthetic look (tags simulated): P on all 31 with verdicts (the primary, nothing deviated), P on the 15 "
      "frozen confirm countries with the same F constants and labels for information only, no E (e_specs.py "
      "absent), the vintage report", ok, f"{t.__name__ if t else ''} {msg[:120]}" if not ok
      else f"model verdict {look['primary']['model_verdict']}")
if look is not None:
    mde = look["mde"]
    ve = ([full["tests"][k]["verdict_eligible"] for k in specs.PRIMARY]
          + [full["tests"][k]["verdict_eligible"] for k in ("C3a", "C3b")]
          + [v.get("verdict_eligible") for v in full["secondary"].values()]
          + [v.get("verdict_eligible") for v in full["robustness"].values()])
    np_ = len(specs.PRIMARY)
    check("J6 verdict_eligible is True for the eight primary tests only (False for C-3's legs, every secondary and "
          "robustness result)", ve[:np_] == [True] * np_ and all(v is False for v in ve[np_:]),
          f"{len(ve) - np_} non-primary results")
    proj = [mde[k]["mde_full_sample_projected"] for k in specs.PRIMARY if k != "C3"]
    proj += [mde["C3"][leg]["mde_full_sample_projected"] for leg in ("C3a", "C3b")]
    ratio = [mde[k]["mde_full_sample_projected"] / mde[k]["mde_explore_half"] for k in specs.PRIMARY if k != "C3"]
    check("J7 the MDE report: the explore half's MDE and its projection to the full sample for every test, C-3 by leg; "
          "the projection is smaller (fewer clusters' se scaled by sqrt(G_explore / G_full), t with G_full - 1 df)",
          all(x is not None and math.isfinite(x) for x in proj) and all(0.4 < q < 1 for q in ratio),
          "projected / explore: " + ", ".join(f"{q:.2f}" for q in ratio))
    prim2 = confirm.primary(look["P_full_sample"], rep, deviated={"C2", "D2"})
    mixed = {k: (rep["tests"][k] if k in ("C2", "D2") else full["tests"][k]) for k in specs.PRIMARY}
    lab, mv = specs.verdicts(mixed)
    check("J8 the bug policy (section 7): a deviated test's primary is the confirm half's result, Holm runs over the "
          "family with the substituted p-values, the full sample is labelled exploratory",
          prim2["tests"]["C2"]["p"] == rep["tests"]["C2"]["p"] and prim2["tests"]["D2"]["geos_used"] == rep["tests"]["D2"]["geos_used"]
          and prim2["tests"]["C1"]["p"] == full["tests"]["C1"]["p"] and prim2["verdicts"] == lab
          and prim2["model_verdict"] == mv and prim2["full_sample_exploratory"] == ["C2", "D2"]
          and prim2["source"]["C2"].startswith("confirm half"), str(prim2["source"]))
for k, v in REAL.items():
    setattr(es, k, v)
build.fetch = real_fetch
build.reset()
shutil.rmtree(TMP, ignore_errors=True)
check("J5 no network call was attempted during the whole check", len(NET) == 0, f"{len(NET)} attempts")
check("J9 the real fetch log is untouched by the whole check", (open(es.LOG, "rb").read() if os.path.exists(es.LOG)
                                                             else b"") == log_before)

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
