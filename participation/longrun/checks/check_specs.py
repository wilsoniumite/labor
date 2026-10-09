# check_specs.py — unit checks of the rules the code-review of 2026-10-09 found unguarded (synthetic data only; no
# long-run value is read; the network is blocked).
#   (a) post-freeze segments never enter a primary frame: the primary frames are identical with and without them, and
#       only the robustness row 'with post-freeze segments' carries them (and runs when they exist);
#   (b) the Kholodilin coding reaches the panel: strict 1/0 where covered, NaN where not; a covered strict year is
#       dropped by both the control-era qualifier and the strict-control robustness row; uncovered countries are listed;
#       the census frame carries strict;
#   (c) a degenerate design: every robustness row and qualifier is guarded on its own (one inestimable run never wipes
#       the others), and run() completes;
#   (d) the co-primary RI: an observed contrast t that cannot be computed gives p NaN (never a silent 0) and the verdict
#       statistic is then NaN; a nuisance slope left unidentified does not stop the contrast t (computed by
#       partialling out); in exact mode a non-finite assignment makes p NaN; t_contrast equals the frozen WCR's t;
#   (e) the curvature qualifier's time terciles come from the ranking set (q alone), not from the estimation rows;
#   (f) leave-one-out: every country's row is reported; the US row by name; the US wording whenever the US row alone
#       crosses 0.10, even when another country is worst;
#   (g) Holm over the frozen families: a frozen member that errors takes p = 1 inside its family;
#   (h) the confirm-half replication reports LR-K2 for information below the testability floor (>= 2 per group);
#   (i) D2-L carries its series-permutation placebo; the pooled D1 of the two studies is reported (no verdict);
#   (j) q by the FROZEN ladder: a flagged interior JST year is NaN inside its run and moves neither the run nor the
#       segment, and rung 2 still extends it; the ladder is never recomputed from values;
#   (k) coverage: C-6L and LR-C1 are counted inside outcome segments too; Mexico 2015 (a survey) is not an Extract B
#       census; the US deep study's analyses run on synthetic tables (AD-1 census points their own segment, not
#       overwriting AD-3; U in U-C1; five-year differences for every analysis with 4 Newey-West lags; by sex);
#   (l) the blinded debugging panel permutes q paths across countries.
#
# Run from longrun/:  ../../venv/Scripts/python.exe checks/check_specs.py      Exit status 0 only if all pass.

from __future__ import annotations

import io
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
import requests  # noqa: E402
import build  # noqa: E402
import coverage as cv  # noqa: E402
import fetch  # noqa: E402
import inference_l as infl  # noqa: E402
import segments as sg  # noqa: E402
import specs  # noqa: E402

inf = specs.inf
RESULTS = []
NET = []


def _blocked(*a, **k):
    NET.append(1)
    raise RuntimeError("network call attempted")


requests.adapters.HTTPAdapter.send = _blocked
socket.create_connection = _blocked
socket.socket.connect = _blocked


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ---------------------------------------------------------------- a synthetic world
GEOS = ["US", "CA", "DE", "FR", "NL", "CL", "CO", "CR", "MX", "IL"]
HIGH = {"CL", "CO", "CR", "MX", "IL"}


def make_data(seed=3, years=range(1961, 1996), strict=True, plant=-8.0) -> specs.Data:
    rng = np.random.default_rng(seed)
    rows = []
    for c in GEOS:
        q = np.cumsum(rng.normal(0.03, 0.06, len(years) + 1))
        for i, t in enumerate(years):
            x = q[i]
            rows.append(dict(geo=c, year=t, logq_l1=x, qseg_l1=float(years[0] - 1), U=6 + rng.normal(0, 1),
                             e=rng.normal(0, 0.7), school2024=40 + rng.normal(0, 1), cohort=0.5 + rng.normal(0, 0.01),
                             strict=(float(t <= 1970) if c in ("US", "DE", "FR") else np.nan) if strict else np.nan))
    cy = pd.DataFrame(rows).set_index(["geo", "year"])
    kn = specs.knots(cy[["logq_l1", "qseg_l1"]], {c: (years[0] - 1, years[-1]) for c in GEOS}, unseen_only=False)
    P = np.zeros((len(cy), 3))
    for i, (g, t) in enumerate(cy.index):
        k = kn[g]
        P[i] = specs.basis([cy.loc[(g, t), "logq_l1"]], k["k1"], k["k2"])[0]
    h = np.array([1.0 if g in HIGH else 0.0 for g in cy.index.get_level_values(0)])
    base = 70 - 0.3 * cy["U"].to_numpy() + cy["e"].to_numpy() + 5 * P[:, 0] + plant * h * P[:, 2]
    for col in ("A2534", "A2534_M", "A2534_F", "A5564", "AW2554", "AM2554"):
        cy[col] = base + rng.normal(0, 0.2, len(cy))
    for col in ("A2534", "A2534_M", "A2534_F", "A5564", "AW2554", "AM2554", "U", "logq_l1", "school2024", "cohort",
                "strict", "logq_hpi_l1"):
        if col not in cy:
            cy[col] = np.nan
        cy[col + "__breaks"] = [[] for _ in range(len(cy))]
    cy["qseg_hpi_l1"] = np.nan
    cl = pd.DataFrame({"geo": GEOS, "F_L": [60 if c in HIGH else 20 for c in GEOS],
                       "F_L_2029": [55 if c in HIGH else 25 for c in GEOS],
                       "F_L_1970": [58 if c in HIGH else 22 for c in GEOS], "F_L_1970_year": [1970] * len(GEOS),
                       "F_L_flagged": [c == "DE" for c in GEOS], "GN": np.nan}).set_index("geo")
    H = specs.compute_H(cl["F_L"].to_dict(), GEOS)
    members = {"K2": GEOS, "Y0": GEOS, "C6L": GEOS, "C1": []}
    return specs.Data(cy, cl, {"q": kn}, H, members, families={"K": ["LR-K2"], "C-L": ["LR-Y0", "C-6L"]},
                      kh_uncovered=[c for c in GEOS if c not in ("US", "DE", "FR")])


B, R = 199, 199
D = make_data()

# ---------------------------------------------------------------- (a) post-freeze segments
print("(a) post-freeze segments")
post = pd.DataFrame([dict(geo="US", series="lfs", tau=1980, reason="x", citation="y"),
                     dict(geo="CL", series="q", tau=1984, reason="x", citation="y")], columns=sg.COLUMNS)
D2 = specs.Data(D.cy, D.cl, D.knots, D.H, D.members, post_seg=post, families=D.families, kh_uncovered=D.kh_uncovered)
f1, f2 = specs.basis_frame(D, GEOS), specs.basis_frame(D2, GEOS)
l1, l2 = specs.linear_frame(D, "C-6L", GEOS), specs.linear_frame(D2, "C-6L", GEOS)
check("A1 the primary frames are identical with and without post-freeze rows (basis and linear)",
      f1.attrs["breaks"] == f2.attrs["breaks"] and l1.attrs["breaks"] == l2.attrs["breaks"] and f1.equals(f2))
fp = specs.basis_frame(D2, GEOS, post=True)
check("A2 the post-freeze frame carries the rows (lfs from tau, lagged q from tau + 1)",
      ("US", 1980) in fp.attrs["breaks"] and ("CL", 1985) in fp.attrs["breaks"], str(fp.attrs["breaks"]))
rob = specs.robustness(D2, D2.H, D2.members, B, R, inf.SEED)
pf = {k: v for k, v in rob.items() if k.startswith("post_freeze_segments.")}
check("A3 the robustness row 'with post-freeze segments' runs when rows exist (LR-K2, LR-Y0, C-6L; LR-C1 without "
      "Extract B reports why)", {"post_freeze_segments.LR-K2", "post_freeze_segments.LR-Y0",
                                  "post_freeze_segments.C-6L"} <= set(pf)
      and all("error" not in pf[k] for k in ("post_freeze_segments.LR-K2", "post_freeze_segments.C-6L")), str(
          {k: v.get("error") for k, v in pf.items()}))
rob0 = specs.robustness(D, D.H, D.members, B, R, inf.SEED)
check("A4 without post-freeze rows the row does not run", not any(k.startswith("post_freeze") for k in rob0))

# ---------------------------------------------------------------- (b) Kholodilin
print("(b) the Kholodilin coding")
kh = pd.DataFrame([dict(geo="US", year=y, strict=int(y <= 1952)) for y in range(1950, 2026)])
raw = {"kholodilin": kh}
s = build.kholodilin_frame(kh)
check("B1 kholodilin_frame maps the coding to strict 1/0 by (geo, year)", s.loc[("US", 1951)] == 1
      and s.loc[("US", 1960)] == 0)
check("B2 the uncovered countries are listed", build.kholodilin_uncovered(raw, ["US", "FR", "CL"]) == ["CL", "FR"])
q2 = D.cy.reset_index()
cen = build.census(pd.DataFrame(dict(geo=["US", "FR"], year=[1980, 1980], sample=["a", "b"], R=[10.0, 12.0])),
                   q2.assign(strict=[1.0] * len(q2)), pd.DataFrame(columns=sg.COLUMNS))
check("B3 the census frame carries strict (LR-C1's strict-control row has its column)", "strict" in cen
      and cen["strict"].notna().all())
M = specs.basis_frame(D, sorted(D.H))
base = specs.k2_core(M, D.H, B, R)
lab = "supported" if base["p_stat"] < 0.05 else "contradicted"
kq = specs.k2_qualifiers(D, M, D.H, base, lab, B, R, inf.SEED, None)
ce = kq["rests on control-era years"]
nstrict = int((M["strict"] == 1).sum())
check("B4 the control-era qualifier drops every covered strict year", ce["run"] is not None
      and ce["run"].get("n_strict_dropped") == nstrict and nstrict > 0
      and ce["run"].get("n") == base["n"] - nstrict, f"{ce['run']}")
sr = rob0["strict_control_dropped.LR-K2"]
check("B5 the strict-control robustness row drops them too, and the uncovered countries are reported",
      "error" not in sr and sr["n"] == base["n"] - nstrict
      and rob0["strict_control_dropped.uncovered_countries"] == D.kh_uncovered, str(sr.get("n")))

# ---------------------------------------------------------------- (c) degenerate design
print("(c) a degenerate design")
cyd = D.cy.copy()
cyd["A2534_F"] = np.nan                                  # women-only rows: none
cyd = cyd.drop(columns=["cohort"])
Dd = specs.Data(cyd, D.cl.drop(columns=["F_L_1970_year"]), D.knots, D.H, D.members, families=D.families)
robd = specs.robustness(Dd, Dd.H, Dd.members, B, R, inf.SEED)
errs = {k: v["error"] for k, v in robd.items() if isinstance(v, dict) and "error" in v}
check("C1 one inestimable or column-less run is that row's error; the other rows still run",
      "error" not in robd and "women_only.LR-K2" in errs and "error" not in robd["men_only.LR-K2"]
      and "error" not in robd["F_L_2029.LR-K2"], str(sorted(errs)))
out = specs.run(Dd, B=B, R=R, with_ci=False)
check("C2 run() completes on it, with LR-K2's qualifiers reported", "LR-K2" in out["verdicts"]
      and "qualifier_runs" in out["tests"]["LR-K2"])

# ---------------------------------------------------------------- (d) the RI
print("(d) the co-primary RI")
x, Zr = infl.contrast(specs._k2_X(M, D.H), specs.DID)
Zc = specs._Z(M, ["geo", "year"], ["U"])
w = inf.wcr(M["y"].to_numpy(float), x, np.column_stack([Zc, Zr]), M["geo"].to_numpy(), side=-1, B=99)
ct = infl.ContrastT(M["y"], M[["P1", "P2", "P3"]].to_numpy(float), Zc, M["geo"])
Hv = np.array([D.H[u] for u in ct.labels], float)
b_, se_, t_ = ct.t_contrast(ct.W(infl.floor_weights(Hv)), specs.DID)
check("D1 the partialled-out contrast t equals the frozen WCR's t on the rewritten regression",
      math.isclose(t_, w["t"], rel_tol=1e-8) and math.isclose(se_, w["se"], rel_tol=1e-8), f"{t_} vs {w['t']}")
Mn = M.copy()
lowc = [c for c in sorted(D.H) if not D.H[c]]
Mn.loc[Mn["geo"].isin(lowc), "P2"] = 0.0                 # no low-floor P2 variation: g2 unidentified
ctn = infl.ContrastT(Mn["y"], Mn[["P1", "P2", "P3"]].to_numpy(float), specs._Z(Mn, ["geo", "year"], ["U"]),
                     Mn["geo"])
old_t = ctn.t(ctn.W(infl.floor_weights(Hv)), specs.DID)[2]
ri = infl.ri_h(ctn, Hv, specs.DID, R=R)
check("D2 an unidentified nuisance slope does not stop the contrast: the old full-W t is NaN, the partialled-out t is "
      "finite and the RI p is a real p (not 0 from NaN comparisons)", not np.isfinite(old_t) and np.isfinite(ri["t"])
      and 0 < ri["p_lower"] <= 1 and ri["n_nonfinite"] >= 0, f"old {old_t}; t {ri['t']}; p {ri['p_lower']}; "
                                                              f"nonfinite {ri['n_nonfinite']}")
Mz = M.copy()
Mz.loc[Mz["geo"].isin([c for c in sorted(D.H) if D.H[c]]), "P3"] = 0.0     # high-floor P3 constant: DiD unidentified
ctz = infl.ContrastT(Mz["y"], Mz[["P1", "P2", "P3"]].to_numpy(float), specs._Z(Mz, ["geo", "year"], ["U"]),
                     Mz["geo"])
riz = infl.ri_h(ctz, Hv, specs.DID, R=R)
check("D3 an observed contrast that is not identified gives p NaN with the reason, never 0",
      not np.isfinite(riz["p_lower"]) and "error" in riz, str({k: riz.get(k) for k in ("t", "p_lower", "error")}))
try:
    kz = specs.k2_core(Mz.pipe(specs._keep_attrs, M), D.H, 99, R)
    okz = not np.isfinite(kz["p_stat"]) and "ri_error" in kz
    lz, uz = specs.labels_for({"LR-K2": {**kz, "testable": True}}, None, {"K": ["LR-K2"]})
    okz = okz and lz["LR-K2"] == "inconclusive" and uz["LR-K2"]["p"] == 1.0
    det = f"p_stat {kz['p_stat']}; {kz.get('ri_error')}"
except ValueError as e:                                   # the WCR itself refuses a collinear contrast: also not silent
    okz, det = True, f"WCR refused: {e}"
check("D4 then the verdict statistic is NaN (never the WCR p alone) and the test takes p = 1 in its family", okz, det)

# ---------------------------------------------------------------- (e) time terciles
print("(e) time terciles from the ranking set")
Mt = M[~((M["geo"] == "US") & (M["year"] >= 1985))].reset_index(drop=True).pipe(specs._keep_attrs, M)
yrs = sorted(D.knots["q"]["US"]["years"])
n = len(yrs)
expect = {t: math.ceil(3 * (r + 1) / n) for r, t in enumerate(yrs)}
t_a = specs.time_tercile_t(Mt, D.H, D.knots["q"])
# the same with the knots' ranking set restricted to the estimation rows (the old rule) gives another t
kn_rows = {c: {**k, "years": sorted(Mt.loc[Mt["geo"] == c, "year"])} for c, k in D.knots["q"].items()}
t_b = specs.time_tercile_t(Mt, D.H, kn_rows)
check("E1 a country with missing outcome years keeps its ranking-set calendar terciles (US 1985-95 all tercile 3 "
      "under the ranking set)", all(expect[t] == 3 for t in range(1985, 1996)) and not math.isclose(t_a, t_b),
      f"{t_a:.4f} vs rows-based {t_b:.4f}")

# ---------------------------------------------------------------- (f) leave-one-out
print("(f) leave-one-out and the US")
loo = {"per_country": {"US": dict(beta=-1.0, p=0.2, p_opposite=0.9), "FR": dict(beta=-1.0, p=0.4, p_opposite=0.9)},
       "max_p": 0.4, "max_p_left_out": "FR", "max_p_opposite": 0.9, "max_p_opposite_left_out": "FR",
       "without_US": dict(beta=-1.0, p=0.2, p_opposite=0.9), "base_beta": -2.0, "n_left_out": 2}
q = specs.cl_qualifier("supported", loo)
check("F1 C-L: the US wording is added whenever the US row alone crosses 0.10, though FR is worst",
      "rests on one country (FR)" in q and specs.US_TEXT in q, q)
real = specs.leave_one_out(D, "LR-Y0", GEOS, B, inf.SEED, None)
check("F2 C-L leave-one-out reports every country's row and the US row by name",
      set(real["per_country"]) == set(GEOS) and real["without_US"] is not None)
lo = kq["rests on one country"]["run"]
check("F3 LR-K2 leave-one-out reports every country's row and the US row by name",
      set(lo["per_country"]) == set(GEOS) and "without_US" in lo)

# ---------------------------------------------------------------- (g) frozen families
print("(g) Holm over the frozen families")
res = {"LR-K2": dict(p_stat=0.01, p_stat_opposite=0.99, beta=-1, testable=True),
       "LR-Y0": dict(p_stat=0.02, p_stat_opposite=0.99, beta=1),
       "C-6L": dict(error="no rows")}
labs, used = specs.labels_for(res, None, {"K": ["LR-K2"], "C-L": ["LR-Y0", "C-6L", "LR-C1"]})
check("G1 an erroring or missing frozen member takes p = 1 in its family (Holm over 3: 0.02 > 0.05/3 fails)",
      labs["LR-Y0"] == "inconclusive" and used["C-6L"]["p"] == 1.0 and used["LR-C1"]["p"] == 1.0,
      f"{labs}")
labs2, _ = specs.labels_for(res, None, {"K": ["LR-K2"], "C-L": ["LR-Y0"]})
check("G2 with the family frozen at one member the same p is supported (the family size is the frozen one)",
      labs2["LR-Y0"] == "supported")

# ---------------------------------------------------------------- (h) replication
print("(h) the confirm-half replication")
Hc = {c: h for c, h in D.H.items() if c in ("US", "CA", "CL", "CO", "MX")}
Dc = specs.Data(D.cy, D.cl, D.knots, Hc, {k: [c for c in v if c in Hc] for k, v in D.members.items()},
                families=D.families)
rp = specs.run(Dc, B=B, R=R, with_ci=False, qualifiers=False, robust=False, replication=True)
k2r = rp["tests"]["LR-K2"]
check("H1 LR-K2 below the testability floor is reported for information (estimate, label for information)",
      "beta" in k2r and k2r.get("information_only") and "LR-K2" in rp["verdicts"], str(k2r.get("information_only")))
pr = specs.run(Dc, B=B, R=R, with_ci=False, qualifiers=False, robust=False)
check("H2 the primary keeps the testability gate", pr["tests"]["LR-K2"]["testable"] is False)

# ---------------------------------------------------------------- (i) D2-L placebo, pooled D1
print("(i) D2-L's placebo; the pooled number")
d2 = out["no_verdict"]["D2-L"]
check("I1 D2-L reports its series-permutation placebo (central 80% and where the observed t falls)",
      "placebo" in d2 and len(d2["placebo"].get("central80", [])) == 2 and d2["placebo"]["draws"] > 100,
      str(d2.get("placebo", {}).get("draws")))
pdl = out["no_verdict"]["pooled_D1_two_studies"]
check("I2 the inverse-variance pooled D1 of the two studies is reported, no verdict", "beta" in pdl
      and "verdict" not in pdl and pdl["se"] > 0, str(pdl))

# ---------------------------------------------------------------- (j) the frozen ladder
print("(j) q by the frozen ladder")
yrs_j = list(range(1950, 2021))
jst = pd.DataFrame(dict(geo="US", year=yrs_j, hpnom=[1.0 + 0.01 * i for i in range(len(yrs_j))],
                        housing_rent_yd=0.05, housing_capgain=0.0, housing_capgain_ipol=0,
                        rent_ipolated=[1 if y == 1975 else 0 for y in yrs_j], cpi=1.0))
house = pd.DataFrame(dict(geo="US", year=list(range(1950, 2026)), value=1.0, flag="", MEASURE="RPI",
                          UNIT_MEASURE="IX"))
cpi = pd.DataFrame(dict(geo="US", year=list(range(1950, 2026)), value=1.0, flag="", METHODOLOGY="N", MEASURE="CPI",
                        UNIT_MEASURE="IX", EXPENDITURE="_T", ADJUSTMENT="N", TRANSFORMATION="_Z"))
frozen = {"US": {y: "jst" for y in yrs_j} | {y: "rpi/cpi" for y in range(2021, 2026)}}
seg0 = pd.DataFrame(columns=sg.COLUMNS)
qp, _ = build.q_panel({"house": house, "cpi": cpi, "jst": jst}, ["US"], seg0, "rent", frozen)
qv = qp.set_index("qyear")
check("J1 a flagged interior JST year is NaN inside its run; the run, its source and segment stay (no split); rung 2 "
      "extends from JST's last year", np.isnan(qv.loc[1975, "logq"]) and qv.loc[1976, "src"] == "jst"
      and qv.loc[1974, "seg"] == qv.loc[1976, "seg"] == 1950 and qv.loc[2021, "src"] == "rpi/cpi",
      str(qv.loc[[1974, 1975, 1976, 2021], ["src", "seg"]].to_dict()))
qv2, _ = build.q_panel({"house": house, "cpi": cpi, "jst": jst}, ["US"], seg0, "rent", None)
qv2 = qv2.set_index("qyear")
check("J2 (contrast) the old value-based ladder would have split the run at the flagged year",
      1975 not in qv2.index or qv2.loc[1976, "seg"] != 1950)

# ---------------------------------------------------------------- (k) coverage, samples, US study
print("(k) coverage, samples and the US study")
seg_k = pd.DataFrame([dict(geo="US", series="school", tau=2000, reason="x", citation="y")], columns=sg.COLUMNS)
raw_k = {sid: {str(y): ["US"] for y in range(1990, 2026)} for sid in cv.PROBES}
smp_k = {"roles": {}, "extract_B": [dict(sample="us1980a", country="US", year=1980, relate=True),
                                    dict(sample="us1990a", country="US", year=1990, relate=True)]}
saved = dict(cv.ILO_DOC_START)
cv.ILO_DOC_START["US"] = 1999
cube_k, tab_k = cv.eligibility(raw_k, smp_k, seg_k)
cv.ILO_DOC_START.clear()
cv.ILO_DOC_START.update(saved)
r_us = tab_k.set_index("geo").loc["US"]
check("K1 C-6L counts inside one outcome segment: a school break in 2000 leaves the larger piece (2001-2025 bar "
      "2020-21) only", int(r_us["C6L_n_in_one_segment"]) == len([t for t in range(2000, 2026)
                                                                 if t not in (2020, 2021)]), str(r_us["C6L_n_in_one_segment"]))
smp = json.load(open(cv.SAMPLES, encoding="utf-8"))
check("K2 Mexico 2015 (the Encuesta Intercensal, a survey) is not an Extract B census; every sample records its kind",
      "mx2015a" not in {r["sample"] for r in smp["extract_B"]}
      and all("kind" in r for r in smp["F_L"] + smp["extract_B"]))
import us_study  # noqa: E402


def xls(df):
    b = io.BytesIO()
    df.to_excel(b, index=False, header=False)
    return b.getvalue()


ad3 = pd.DataFrame([["Year", "Men: child of householder", "Women: child of householder"]]
                   + [[str(y), 15 + 0.1 * (y - 1967), 9 + 0.1 * (y - 1967)] for y in range(1967, 2016)])
ad1 = pd.DataFrame([["Year", "Men child", "Women child"]]
                   + [[str(y), 30.0, 20.0] for y in (1960, 1970, 1980)] + [[str(y), 18.0, 12.0] for y in range(2016, 2025)])
enr = pd.DataFrame([["Year", "20 and 21 years", "22 to 24 years"]] + [[str(y), 30 + 0.2 * (y - 1959), 15.0]
                                                                     for y in range(1959, 2025)])
tables = {"ad3_25_34": xls(ad3), "ad1": xls(ad1), "enroll02": xls(enr)}
rng = np.random.default_rng(5)
years_u = list(range(1947, 2026))


def fake_series(half="explore"):
    d = pd.DataFrame({k: 70 + rng.normal(0, 1, len(range(1948, 2026))) for k in us_study.PART},
                     index=range(1948, 2026))
    d["U"] = 5 + rng.normal(0, 1, len(d))
    d["logq_l1"] = np.cumsum(rng.normal(0.01, 0.02, len(d)))
    return d, {}


saved_fs, saved_cu = us_study.fetch_series, fetch.census_us
us_study.fetch_series = fake_series
fetch.census_us = lambda table, half: tables[table]
try:
    cor = us_study.coresidence()
    usr = us_study.run()
finally:
    us_study.fetch_series, fetch.census_us = saved_fs, saved_cu
both = cor[cor["year"] == 1970]
check("K3 the US study keeps AD-1's census points beside AD-3's (1970: both rows, AD-3's value not overwritten)",
      set(both["series"]) == {"AD-3", "AD-1 census"}
      and math.isclose(float(both.loc[both["series"] == "AD-3", "men"].iloc[0]), 15.3), str(both.to_dict("records")))
keys = set(usr)
check("K4 U-C1 with the cycle, by sex; five-year differences for every analysis; Newey-West 4 lags",
      {"U-C1.both", "U-C1.men", "U-C1.women", "U-C1.both.five_year", "U-K2.both.five_year", "U-Y0.both.five_year",
       "U-S", "U-S.five_year"} <= keys and "b_U" in usr["U-C1.both"] and usr["newey_west_lags"] == 4
      and us_study.NW_LAGS == 4, str(sorted(keys))[:300])

# ---------------------------------------------------------------- (l) blinded debugging
print("(l) the blinded debugging panel")
Db = specs.blind(D, seed=12345)
moved = sum(not np.allclose(Db.cy.xs(c, level=0)["logq_l1"].to_numpy(float), D.cy.xs(c, level=0)["logq_l1"]
                            .to_numpy(float), equal_nan=True) for c in GEOS)
check("L1 the blinded panel gives every country another country's q path, knots recomputed by the rule",
      moved == len(GEOS) and all(Db.knots["q"][c]["k1"] is not None for c in GEOS))

check("Z1 no network call was attempted during the whole check", not NET, f"{len(NET)}")
n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks pass")
sys.exit(1 if n_fail else 0)
