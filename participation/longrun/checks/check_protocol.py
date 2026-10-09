# check_protocol.py — the long-run pipeline against longrun/PROTOCOL.md, line by line.
#   (a) the tests: TRANSCRIPTION below is copied by hand from PROTOCOL.md section 5 (compare it with the protocol, line
#       by line); specs.TESTS, FAMILIES, NO_VERDICT, ROBUSTNESS (ten rows), K2_QUALIFIERS and the constants must match it;
#   (b) the measures: build.MANIFEST's keys against L4-L6's key strings; fetch's L1/L2 window rule; the strata and seed
#       of section 4; the IPUMS extract whitelist of L9;
#   (c) the basis (section 5): knots by the tercile rule on a toy series; P1 + P2 + P3 = x; the continuity of the broken
#       line; the invariance check (a constant added to x inside the segment shifts both knots, leaves P2 and P3
#       unchanged and shifts P1 by the constant); fewer than 6 ranked years -> no knots; the ranking set uses q alone;
#   (d) H (L9): top half by F, odd middle low, ties by code; the 'not testable' rule (8 countries, 3 per group);
#   (e) the contrast rewrite: DiD from the rewritten regression equals the contrast of the full regression's slopes;
#   (f) the verdict rules: Holm within families, calibration only makes a verdict harder (max(raw, calibrated)), the
#       drop condition, the model-level readings, the reading table, LR-Y0's reading note, the joint reading table,
#       the US wording of the leave-one-out qualifier, qualifiers never change labels;
#   (g) segments: data/segments.csv valid (a reason and a citation for every row), built from the documented rows plus
#       the ladder's switches; the dummies act from tau (tau + 1 for lagged q);
#   (h) coverage: the ladder ('extend, don't fill'), the chosen segment rule, the testability counts of
#       data/coverage_l2.csv recomputed from data/coverage.json.
# The network is blocked for the whole run.
#
# Run from longrun/:  ../../venv/Scripts/python.exe checks/check_protocol.py      Exit status 0 only if all pass.

from __future__ import annotations

import json
import math
import os
import socket
import sys

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LROOT, "code"))
import fetch  # noqa: E402
import requests  # noqa: E402
import build  # noqa: E402
import coverage as cv  # noqa: E402
import inference_l as infl  # noqa: E402
import ipums  # noqa: E402
import segments as sg  # noqa: E402
import skeleton  # noqa: E402
import specs  # noqa: E402
import split as sp  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


NET = []


def _blocked(*a, **k):
    NET.append(1)
    raise RuntimeError("network call attempted")


requests.adapters.HTTPAdapter.send = _blocked
socket.create_connection = _blocked
socket.socket.connect = _blocked

# ---------------------------------------------------------------- (a) transcription of PROTOCOL.md section 5
# Copied by hand from PROTOCOL.md, section 5 ('K: the distinctive test', 'C: consistency checks', 'No verdict',
# 'Verdicts', 'Robustness'). One row per test: outcome, tested quantity, controls, fixed effects, predicted sign,
# inference, family, membership rule.
TRANSCRIPTION = {
    "LR-K2": dict(outcome="A2534", controls=["U"], fe=["geo", "year"], side=-1, family="K", members="K2",
                  basis=True, inference="wcr + ri (co-primary)"),       # 'H1: DiD < 0'; RI co-primary
    "LR-Y0": dict(outcome="A2534", controls=["U"], fe=["geo", "year"], side=1, family="C-L", members="Y0",
                  basis=True, inference="wcr"),                          # 'H1: g1 > 0'
    "C-6L": dict(outcome="school2024", controls=[], fe=["geo", "year"], side=1, family="C-L", members="C6L",
                 basis=False, inference="wcr"),                          # 'the regressor is the cycle'
    "LR-C1": dict(outcome="R", controls=[], fe=["geo", "round"], side=1, family="C-L", members="C1", basis=False,
                  inference="wcr"),                                      # 'Round fixed effects ... No cycle control'
}
FAMILIES_T = {"K": ["LR-K2"], "C-L": ["LR-Y0", "C-6L", "LR-C1"]}
NO_VERDICT_T = {"D1-L": ("A2534", "Q*F"), "D2-L": ("A2534", "sqdev(Q)"), "C-2L": ("A2534-A5564", "Q"),
                "C-3L.diff": ("AW2554-AM2554", "Q"), "C-3L.women": ("AW2554", "Q"), "E-SCH1-L": ("school2024", "U_l1")}
ROBUSTNESS_T = {"giuliano_nunn": {"LR-K2", "D1-L"}, "F_L_2029": {"LR-K2"}, "F_L_continuous": {"LR-K2"},
                "men_only": {"LR-K2", "LR-Y0"}, "women_only": {"LR-K2", "LR-Y0"},
                "strict_control_dropped": {"LR-K2", "LR-Y0", "LR-C1"}, "q_hpi": {"LR-K2", "LR-Y0", "LR-C1"},
                "F_L_1970_later_years": {"LR-K2", "D1-L"}, "flagged_samples_dropped": {"LR-K2", "D1-L"},
                "post_freeze_segments": {"LR-K2", "LR-Y0", "C-6L", "LR-C1"}}
QUALIFIERS_T = ["rests on one country", "rests on floor-group trends", "rests on cohort size",
                "rests on control-era years", "indistinguishable from time curvature"]
print("(a) the tests against the transcription")
for k, t in TRANSCRIPTION.items():
    s = specs.TESTS[k]
    diff = {f: (s.get(f), v) for f, v in t.items() if s.get(f) != v}
    check(f"A1 {k}: outcome, controls, fixed effects, sign, family, membership, basis, inference", not diff, str(diff))
check("A2 no test beyond the protocol's four", set(specs.TESTS) == set(TRANSCRIPTION))
check("A3 families: K = {LR-K2}; C-L = {LR-Y0, C-6L, LR-C1}", specs.FAMILIES == FAMILIES_T)
check("A4 the no-verdict list (D1-L, D2-L, C-2L, C-3L both legs, E-SCH1-L)",
      {k: (v["outcome"], v["x"]) for k, v in specs.NO_VERDICT.items()} == NO_VERDICT_T)
check("A5 the robustness table: ten rows, each applied to the protocol's tests",
      len(specs.ROBUSTNESS) == 10 and {k: set(v) for k, v in specs.ROBUSTNESS.items()} == ROBUSTNESS_T)
check("A6 LR-K2's five mechanical qualifiers", specs.K2_QUALIFIERS == QUALIFIERS_T)
check("A7 constants: alpha 0.05, LOO 0.10 (frozen), B 9999, at least 6 ranked years, LR-K2 needs 8 countries and 3 "
      "per group, the drop condition at 5%, 999 placebo draws, DiD = (1, 0, -1, -1, 0, 1)",
      (specs.ALPHA, specs.LOO_P, specs.B_DEFAULT, specs.MIN_RANKED, specs.MIN_K2_COUNTRIES, specs.MIN_K2_GROUP,
       specs.DROP_SIG, specs.PLACEBO_DRAWS, specs.DID) == (0.05, 0.10, 9999, 6, 8, 3, 0.05, 999, (1, 0, -1, -1, 0, 1)))
check("A8 the skeleton: rho 0.5 and 0.9 for calibration (2000 null replications each), rho 0.7 for MDEs",
      (skeleton.RHOS_CAL, skeleton.RHO_MDE, skeleton.R_CAL) == ((0.5, 0.9), 0.7, 2000))
check("A9 the model-level readings (section 5 'Verdicts') word for word",
      specs.MODEL_READINGS["favours"] == "favours the floor mechanism against the no-coresidence and attenuation "
                                         "accounts"
      and specs.MODEL_READINGS["against"] == "against the floor mechanism together with its stated regime placement "
                                             "and auxiliaries 1-3"
      and specs.MODEL_READINGS["consistent"].startswith("consistent with the floor mechanism or with an attenuated"))
check("A10 a supported LR-K2 carries the sentence on Kaplan/Ermisch-type models (section 2)",
      "Kaplan" in specs.KAPLAN_SENTENCE and "not distinctive" in specs.KAPLAN_SENTENCE)

# ---------------------------------------------------------------- (b) measures
print("(b) the measures")
M = build.BY_ID
check("B1 L4: activity rates LF_RATE / PT_POP_SUB / F, M / LF, with Y25T29 and Y30T34 (and the 55-64 and 25-54 bands)",
      M["act"]["source"] == "oecd_lfs" and M["act"]["key"]["MEASURE"] == "LF_RATE"
      and M["act"]["key"]["UNIT_MEASURE"] == "PT_POP_SUB" and set(M["act"]["key"]["SEX"]) == {"F", "M"}
      and {"Y25T29", "Y30T34", "Y55T59", "Y60T64"} <= set(M["act"]["key"]["AGE"])
      and M["act"]["key"]["LABOUR_FORCE_STATUS"] == "LF")
check("B2 L5: the cycle UNE_RATE / PT_LF_SUB / _T / Y25T54 / UNE from the same flow",
      M["une"]["key"] == {"MEASURE": "UNE_RATE", "UNIT_MEASURE": "PT_LF_SUB", "SEX": "_T", "AGE": "Y25T54",
                          "LABOUR_FORCE_STATUS": "UNE"} and M["une"]["source"] == "oecd_lfs")
check("B3 L6 rung 2: RPI (and HPI) A / IX from DF_HOUSE_PRICES; CPI A.N.CPI.IX._T.N._Z from DF_PRICES_ALL and "
      "DF_PRICES_C2018_ALL",
      M["house"]["key"] == {"FREQ": "A", "MEASURE": ["RPI", "HPI"], "UNIT_MEASURE": "IX"}
      and M["cpi"]["key"] == M["cpi2018"]["key"] == build.CPI_KEY
      and fetch.SOURCES["oecd_cpi2018"]["flow"].endswith("DF_PRICES_C2018_ALL,1.0"))
check("B4 L6: the C2018 flow is not queried for AT, CO, DE, IL, KR, NZ, PL, SK, UK, US (the protocol's list)",
      set(M["cpi2018"]["absent"]) == set("AT CO DE IL KR NZ PL SK UK US".split()))
check("B5 L4: DE's outcome and cycle come from DEU_F, its prices from DEU",
      fetch.ref_area("DE", "oecd_lfs") == "DEU_F" and fetch.ref_area("DE", "oecd_rpi") == "DEU")
check("B6 L6: JST rent index = yield x hpnom, or x cumulated capital gains for ES, IT, PT",
      build.CAPGAIN_Q == ("ES", "IT", "PT"))
win_ok = (fetch.window("FR") == list(range(1950, 1995)) and 2020 not in fetch.window("US")
          and 2021 not in fetch.window("US") and fetch.window("US")[-1] == 2025
          and fetch.window("CZ") == list(range(1991, 1995)) and fetch.window("DE")[-1] == 1994
          and not fetch.is_unseen("BG", 1990) and not fetch.is_unseen("RO", 1990))
check("B7 L1/L2: European members 1950-1994 (1995-1996 were seen by the European study); others 1950-2025 without "
      "2020-21; transition members from 1991; non-members never", win_ok)
check("B8 section 4: strata, the forced US placement and the seed string",
      fetch.STRATA["Anglo"] == ["IE", "UK", "US", "CA", "AU", "NZ"] and fetch.STRATA["Asia"] == ["JP", "KR"]
      and fetch.STRATA["Latin America"] == ["MX", "CL", "CO", "CR"] and fetch.FORCED_EXPLORE == "US"
      and sp.seed_of(["A", "B"]) == int(__import__("hashlib").sha256(b"participation-longrun-split-v1|A,B")
                                        .hexdigest()[:16], 16))
check("B9 L9: the extract whitelist holds her variables and RELATED; no labour, education, income, marital-status or "
      "tenure variable", set(ipums.HER_VARS) == {"COUNTRY", "YEAR", "SAMPLE", "SERIAL", "PERNUM", "HHWT", "PERWT",
                                                  "AGE", "SEX", "RELATE", "MOMLOC", "POPLOC", "GQ"}
      and "RELATED" in ipums.ALLOWED and not any(v.startswith(("EMP", "LAB", "EDU", "SCHOOL", "INC", "MARST", "OWN"))
                                                 for v in ipums.ALLOWED))
check("B10 L3: OECD OBS_STATUS E, F, M are missing; B is a break",
      all(fetch.is_not_measured(f) for f in "EFM") and not fetch.is_not_measured("B") and fetch.is_break("B")
      and not fetch.is_break(""))

# ---------------------------------------------------------------- (c) the basis
print("(c) the basis")
yrs = list(range(1970, 1982))
x = pd.Series([0.1, 0.5, 0.3, 0.9, 0.2, 0.7, 0.4, 1.1, 0.6, 0.8, 1.0, 0.0], index=yrs)
qf = pd.DataFrame({"logq_l1": x.to_numpy(), "qseg_l1": [1960] * 12},
                  index=pd.MultiIndex.from_arrays([["US"] * 12, yrs], names=["geo", "year"]))
kn = specs.knots(qf, {"US": (1960, 2000)})["US"]
srt = sorted(x)                                                   # n = 12: four per tercile
check("C1 knots: midpoints between terciles (n = 12: 4 per tercile)",
      math.isclose(kn["k1"], (srt[3] + srt[4]) / 2) and math.isclose(kn["k2"], (srt[7] + srt[8]) / 2), str(kn))
P = specs.basis(x.to_numpy(), kn["k1"], kn["k2"])
check("C2 P1 + P2 + P3 = x and the broken line is continuous at the knots",
      np.allclose(P.sum(1), x.to_numpy()) and np.allclose(specs.basis([kn["k1"]], kn["k1"], kn["k2"]).sum(),
                                                          kn["k1"]))
qf2 = qf.copy()
qf2["logq_l1"] += 3.7
kn2 = specs.knots(qf2, {"US": (1960, 2000)})["US"]
P2 = specs.basis(qf2["logq_l1"].to_numpy(), kn2["k1"], kn2["k2"])
check("C3 the invariance check: a constant added to x shifts both knots by it, leaves P2 and P3 unchanged and "
      "shifts P1 by the constant", math.isclose(kn2["k1"], kn["k1"] + 3.7) and np.allclose(P2[:, 1:], P[:, 1:])
      and np.allclose(P2[:, 0] - P[:, 0], 3.7))
short = specs.knots(qf.iloc[:5], {"US": (1960, 2000)})["US"]
check("C4 fewer than 6 ranked years: no knots (the country leaves LR-K2 and LR-Y0)", short["k1"] is None)
qf3 = qf.copy()
qf3["qseg_l1"] = [1960] * 5 + [1976] * 7
kn3 = specs.knots(qf3, {"US": (1960, 2000)})["US"]
check("C5 a seam that arrives with the values (B flag): the longest piece is used", kn3["piece"] == 1976
      and kn3["n"] == 7)
tie = pd.DataFrame({"logq_l1": [0.5] * 6, "qseg_l1": [1960] * 6},
                   index=pd.MultiIndex.from_arrays([["US"] * 6, range(1980, 1986)], names=["geo", "year"]))
tk = specs.knots(tie, {"US": (1960, 2000)})["US"]
check("C6 ties in x are ranked by the earlier year", tk["terciles"] == {"1980": 1, "1981": 1, "1982": 2,
                                                                         "1983": 2, "1984": 3, "1985": 3})

# ---------------------------------------------------------------- (d) H
print("(d) H")
F = {"AT": 30, "CA": 10, "CH": 30, "CL": 60, "CO": 55, "CR": 50, "DE": 20, "FR": 25, "IL": 40}
H = specs.compute_H(F, list(F))
check("D1 H: top half by F (9 countries: 4 high, the middle low), ties by country code",
      sorted(c for c, h in H.items() if h) == ["CL", "CO", "CR", "IL"], str(H))
F2 = {"A1": 5, "A2": 5, "A3": 5, "A4": 5}
check("D2 ties broken by country code (the earlier code ranks higher)",
      specs.compute_H(F2, list(F2)) == {"A1": 1, "A2": 1, "A3": 0, "A4": 0})
check("D3 not testable below 8 countries or 3 per group", not specs.k2_testable({c: i % 2 for i, c in
                                                                                 enumerate("ABCDEFG")})[0]
      and not specs.k2_testable({**{c: 1 for c in "AB"}, **{c: 0 for c in "CDEFGH"}})[0]
      and specs.k2_testable({**{c: 1 for c in "ABC"}, **{c: 0 for c in "DEFGH"}})[0])

# ---------------------------------------------------------------- (e) the contrast rewrite
print("(e) the contrast rewrite")
rng = np.random.default_rng(1)
X = rng.normal(size=(200, 6))
Z = np.column_stack([np.ones(200), rng.normal(size=(200, 3))])
y = X @ np.array([1.0, 0.5, -0.2, 0.3, 0.1, -1.0]) + Z[:, 1:] @ np.array([1, 2, 3]) + rng.normal(size=200)
full = np.linalg.lstsq(np.column_stack([X, Z]), y, rcond=None)[0][:6]
xx, Zr = infl.contrast(X, specs.DID)
re_ = np.linalg.lstsq(np.column_stack([xx, Zr, Z]), y, rcond=None)[0][0]
check("E1 the rewritten regression's tested coefficient is the contrast (1,0,-1,-1,0,1) of the full regression's "
      "slopes", math.isclose(re_, float(np.dot(specs.DID, full)), rel_tol=1e-9), f"{re_} vs {np.dot(specs.DID, full)}")

# ---------------------------------------------------------------- (f) verdict rules
print("(f) verdict rules")


def r(p, po):
    return dict(p_stat=p, p_stat_opposite=po, beta=-1.0)


labs, used = specs.labels_for({"LR-K2": r(0.01, 0.99), "LR-Y0": r(0.02, 0.98), "C-6L": r(0.03, 0.97),
                               "LR-C1": r(0.9, 0.01)}, None)
check("F1 Holm within families: K alone at 0.05; C-L with three (0.02 <= 0.05/3? no: inconclusive chain)",
      labs == {"LR-K2": "supported", "LR-Y0": "inconclusive", "C-6L": "inconclusive", "LR-C1": "contradicted"},
      str(labs))
cal = {"LR-K2": {"rho0.5": {"pred": [0.001, 0.02, 0.04, 0.5], "opp": [0.5]},
                 "rho0.9": {"pred": [0.03, 0.04, 0.06, 0.07], "opp": [0.5]}}}
p, s = specs.calibrated("LR-K2", 0.035, "pred", cal)
check("F2 calibration: the share of null statistics at or below the observed one, at the rho with the larger share; "
      "never below the raw p", math.isclose(p, 0.5) and s == "calibrated"
      and specs.calibrated("LR-K2", 0.9, "pred", cal)[0] >= 0.9)
check("F3 the model-level readings: supported + drop -> favours; supported, no drop -> consistent; contradicted -> "
      "against; else inconclusive; untestable -> not testable",
      specs.model_verdict("supported", True, True) == specs.MODEL_READINGS["favours"]
      and specs.model_verdict("supported", False, True) == specs.MODEL_READINGS["consistent"]
      and specs.model_verdict("contradicted", True, True) == specs.MODEL_READINGS["against"]
      and specs.model_verdict("inconclusive", True, True) == "inconclusive"
      and specs.model_verdict("supported", True, False) == "not testable")
check("F4 the reading table: contradicted and supported stand; inconclusive reads 'no support' at or below the "
      "European benchmark's standardised MDE, 'uninformative' above",
      specs.reading("inconclusive", "C-6L", 0.3, 0.3) == "no support"
      and specs.reading("inconclusive", "C-6L", 0.31, 0.3) == "uninformative"
      and specs.reading("contradicted", "C-6L", 9, 0.1).startswith("stands"))
check("F5 LR-Y0's reading note: strict-control-dropped run significant -> 'consistent with LR-RC attenuation'; not "
      "significant with MDE at/below benchmark -> 'no support'; no Kholodilin coding -> 'uninformative'",
      specs.y0_reading_note(dict(p_stat=0.01, p_stat_opposite=0.99), None, 1, 2) == "consistent with LR-RC attenuation"
      and specs.y0_reading_note(dict(p_stat=0.2, p_stat_opposite=0.8), None, 1, 2) == "no support"
      and specs.y0_reading_note(None, None, 1, 2) == "uninformative")
check("F6 the joint reading table, rows in order",
      specs.joint_reading({"D1": "contradicted"}, specs.MODEL_READINGS["favours"]) == "against the floor mechanism"
      and specs.joint_reading({"D1": "inconclusive"}, specs.MODEL_READINGS["against"]).startswith(
          "against the floor mechanism together with its long-run")
      and specs.joint_reading({}, specs.MODEL_READINGS["favours"]).startswith("supported in the long run")
      and specs.joint_reading({}, specs.MODEL_READINGS["consistent"]).startswith("consistent with the floor")
      and specs.joint_reading({}, "inconclusive") == "inconclusive")
check("F7 the leave-one-out qualifier for the US reads 'rests on the US, a partly seen country'",
      specs.us_wording("rests on one country (US)") == "rests on the US, a partly seen country"
      and specs.us_wording("rests on one country (FR)") == "rests on one country (FR)")
check("F8 the European look's D1 and D2 labels are read for the joint reading",
      specs.europe_labels().get("D1") == "inconclusive" and specs.europe_labels().get("D2") == "inconclusive")
fires = specs.qualifier_fires("supported", -1.0, dict(beta=0.5, p_stat=0.01, p_stat_opposite=0.9), "LR-K2", None)
nofire = specs.qualifier_fires("supported", -1.0, dict(beta=-0.5, p_stat=0.05, p_stat_opposite=0.9), "LR-K2", None)
fires2 = specs.qualifier_fires("supported", -1.0, dict(beta=-0.5, p_stat=0.2, p_stat_opposite=0.9), "LR-K2", None)
check("F9 a qualifier fires on a sign flip or an own-direction p above 0.10, not otherwise", fires and not nofire
      and fires2)

# ---------------------------------------------------------------- (g) segments
print("(g) segments")
seg = sg.load()
doc = pd.read_csv(sg.DOCUMENTED, keep_default_na=False)
check("G1 data/segments.csv is valid: members, series, years, a reason and a citation for every row",
      not sg.validate(seg), str(sg.validate(seg)[:3]))
again = sg.build()
check("G2 data/segments.csv = the documented rows plus the ladder's switches (rebuilt identically)",
      again.reset_index(drop=True).equals(seg.reset_index(drop=True)))
check("G3 every documented row is in the table", len(doc.merge(seg, on=["geo", "series", "tau"])) == len(doc))
br = sg.breaks(seg, ["US"], ["A2534", "logq_l1"])
us_lfs = sorted(seg[(seg["geo"] == "US") & (seg["series"] == "lfs")]["tau"])
us_q = sorted(seg[(seg["geo"] == "US") & (seg["series"] == "q")]["tau"])
check("G4 dummies act from tau for the outcome and from tau + 1 for the lagged q (C3)",
      set(br) == {("US", t) for t in us_lfs} | {("US", t + 1) for t in us_q})
check("G5 the US rows include the 1994 CPS redesign and the 1967 definitions; DE's row records DEU_F",
      {1967, 1994} <= set(us_lfs) and "DEU_F" in " ".join(seg[(seg["geo"] == "DE")]["reason"]))

# ---------------------------------------------------------------- (h) coverage
print("(h) coverage")
cube = json.load(open(cv.CUBE, encoding="utf-8"))
tab = pd.read_csv(cv.L2CSV)
s = {"jst": list(range(1950, 1953)) + list(range(1955, 1991)), "rpi": list(range(1945, 2026)),
     "cpi": list(range(1945, 2021)), "cpi2018": list(range(1990, 2026))}
lad = cv.q_ladder("US", s)
check("H1 'extend, don't fill': the longest JST run overlapping the window (1955-1990) is rung 1; the shorter run "
      "(1950-1952) is not used and the gap before the chosen run is not filled; rung 2 extends forwards from JST's "
      "last year (over the all-items CPI to 2020, then over the COICOP 2018 CPI after its last year)",
      lad.get(1955) == "jst" and lad.get(1990) == "jst" and 1950 not in lad and 1954 not in lad
      and lad.get(1991) == "rpi/cpi" and lad.get(2020) == "rpi/cpi" and lad.get(2021) == "rpi/cpi2018"
      and lad.get(2025) == "rpi/cpi2018", str({k: lad.get(k) for k in (1950, 1954, 1955, 1991, 2020, 2021)}))
gap = cv.q_ladder("US", {"jst": list(range(1952, 1960)) + list(range(1962, 2021)), "rpi": list(range(1945, 2026)),
                         "cpi": list(range(1945, 2026)), "cpi2018": []})
check("H1b rung 2 never fills a gap next to the chosen run (1960-61), and extends backwards only before JST's first "
      "year", 1960 not in gap and 1961 not in gap and gap.get(1962) == "jst" and 1951 not in gap
      and gap.get(2021) == "rpi/cpi", str({k: gap.get(k) for k in (1951, 1959, 1960, 1961, 1962, 2021)}))
only = cv.q_ladder("DE", {"jst": list(range(1962, 2021)), "rpi": list(range(1955, 2026)),
                          "cpi": list(range(1955, 2026)), "cpi2018": []})
check("H1c a run starting at JST's first year is extended backwards by rung 2", only.get(1961) == "rpi/cpi"
      and only.get(1962) == "jst")
segs = cv.q_segments("US", lad, pd.DataFrame(columns=sg.COLUMNS))
check("H2 q segments cut at every source switch", [a for a, _ in segs] == [1955, 1991, 2021], str(segs))
ch = cv.chosen_segment("US", lad, segs)
check("H3 the chosen segment is the longest by its q years with an observation year in the window", ch == (1955, 1990),
      str(ch))
fam = cube["families"]
rec = {k: int(tab[k].sum()) for k in ("K2", "Y0", "C6L", "C1")}
check("H4 data/coverage_l2.csv and data/coverage.json agree on the members of each test", rec == fam["n"],
      f"{rec} vs {fam['n']}")
ok = all(bool(rw["K2"]) == (isinstance(rw["F_L_sample"], str) and bool(rw["F_L_sample"]) and rw["n_eligible"] >= 9)
         for _, rw in tab.iterrows())
check("H5 LR-K2's rule: a frozen F_L sample and at least 9 eligible years inside the chosen segment", ok)
check("H6 LR-Y0's rule: at least 9 eligible years", all(bool(rw["Y0"]) == (rw["n_eligible"] >= 9)
                                                        for _, rw in tab.iterrows()))
check("H7 a test is testable with at least 8 countries", all(fam["testable"][k] == (fam["n"][k] >= 8) for k in fam["n"]))
smp = json.load(open(ipums.SAMPLES, encoding="utf-8"))
check("H8 the frozen IPUMS-I list: census samples 1955-1975 of members; UK's have no RELATE; DE's F_L sample is West "
      "Germany 1970", all(1955 <= r["year"] <= 1975 for r in smp["F_L"])
      and all(not r["relate"] for r in smp["F_L"] if r["country"] == "UK")
      and smp["roles"].get("DE", {}).get("F_L") == "de1970a"
      and not any("survey" in r["note"].lower() for r in smp["F_L"] + smp["extract_B"]))

check("Z1 no network call was attempted during the whole check", not NET, f"{len(NET)}")
n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks pass")
sys.exit(1 if n_fail else 0)
