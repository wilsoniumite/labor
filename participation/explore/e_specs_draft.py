# e_specs_draft.py — DRAFT of code/e_specs.py: the E-hypotheses shortlisted by the explore-half synthesis
# (explore/SYNTHESIS.md). Not frozen and not in code/: the orchestrator decides whether to move it, unchanged, to
# code/e_specs.py before the tag participation-E-freeze.
#
# Contract (code/confirm.py header): run(cy, cl, geos, fstd) -> {id: result}, at most five, each result with keys p and
# p_opposite (one-sided, predicted and opposite direction) and G_star; 'varies' names the P an E varies (an E that
# varies a P never changes that P's verdict). confirm.py runs Holm over these results (specs.holm), on the confirm half.
# cy, cl are build.country_year / build.country_level of the look's download; geos the confirm half; fstd the
# full-sample (31-country) mean and sd of F_raw. Every extra variable is built here from build.fetch's raw frames (the
# frozen manifest's queries, no other data): at the look build.fetch('confirm') is memoised by confirm.py, so nothing
# is downloaded again; on the explore half the draft reads build.fetch('explore') through explore/data.py.
#
# The three E (ranked; see SYNTHESIS.md for the evidence, the forking-paths counts and the power on 15 clusters):
#   E1  'E-HF1'  varies D1. The floor kink with country-specific linear trends and one cycle source for every country:
#                A2534 on log q_{t-1} x F_c, log q_{t-1}, U = lfsa_urgan Y25-74 (citizen TOTAL) for EVERY country,
#                country and year FE, country linear trends ((year-2010)/10), C3 breaks; 1997-2025 without 2020-21.
#                H1: b < 0.
#   E2  'E-OCC1' premise of C-4 (varies no P). On average across countries, the clerical (ISCO-08 OC4) share of
#                employment is higher at 15-24 than at 25-64 (= 15-64 minus 15-24), 2011-2019, stacked rows with
#                country x year FE and young x C3 breaks; a country enters with >= 5 years. H1: b > 0.
#   E3  'E-SCH1' varies C-6. The share of 20-24 in formal education on U(25-54) of the PREVIOUS year (C7's source
#                rule; lagged on the full annual grid before 2020-21 are dropped, as logq_l1 is), country and year
#                FE, C3 breaks; 1997-2025 without 2020-21. H1: b > 0.
# Each result also carries, with no verdict: the leave-one-country-out maximum p (the protocol's qualifier, applied
# to E as to P), the MDE of this run, the explore-half reference values, and the robustness runs named below.
#
# Run the draft on the explore half, from participation/:  ../venv/Scripts/python.exe explore/e_specs_draft.py
# Out (draft only): results/explore_synthesis.json

from __future__ import annotations

import itertools
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = HERE if os.path.basename(HERE) == "code" else os.path.join(os.path.dirname(HERE), "code")
ROOT = os.path.dirname(CODE)
sys.path.insert(0, CODE)
import build  # noqa: E402
import inference as inf  # noqa: E402
import specs  # noqa: E402

B = 9999
LOO_P = specs.LOO_P

# Pre-look references, explore half (16 countries; 15 where F_c is needed), from this file's own run on 2026-10-08.
# The MDE is one-sided 5%, 80% power, from the explore se scaled to 15 clusters (inf.mde, t with 14 df).
EXPLORE_REFERENCE = {
    "E-HF1": dict(beta=-6.094, se=3.208, p=0.0282, n=324, G=15, G_star=6.4, mde_15=8.43, loo_max_p=0.063,
                  units="points of activity per unit of log q x sd(F); sd(F) of the explore half"),
    "E-OCC1": dict(beta=2.077, se=1.116, p=0.0093, n=270, G=15, G_star=13.9, mde_15=2.93, mde_15_country_means=1.82,
                   loo_max_p=0.018, dropped="HR (fewer than 5 years)",
                   units="percentage points of employment share"),
    "E-SCH1": dict(beta=0.415, se=0.165, p=0.0058, n=233, G=16, G_star=8.2, mde_15=0.45, loo_max_p=0.045,
                   units="points of enrolment per point of U(25-54)"),
}


# ---------------------------------------------------------------- shared

def _raw(geos) -> dict:
    """The manifest's raw frames of the half these countries come from (memoised by build.fetch), UK capped (C1)."""
    half = "explore" if set(geos) <= set(build.geos_for("explore")) else "confirm"
    return build.cap_uk(build.fetch(half))


def _put(cy: pd.DataFrame, name: str, s: pd.Series, br: dict) -> pd.DataFrame:
    out = cy.copy()
    s = s[~s.index.duplicated()] if len(s) else s
    out[name] = s.reindex(out.index).to_numpy(float) if len(s) else np.nan
    out[name + "__breaks"] = [list(br.get(g, [])) for g in out.index.get_level_values(0)]
    return out


def _mde15(se, G):
    return inf.mde(se * math.sqrt(G / 15), 15) if se is not None and G else None


def _pick(r: dict) -> dict:
    keys = ("beta", "se", "p", "p_opposite", "n", "G", "G_star", "ci_one_sided", "ci", "mde")
    return {k: r.get(k) for k in keys if k in r}


def _loo(fn, geos_used, side_p="p") -> dict:
    """Leave each country out; the largest one-sided p in each direction and who gives it (PROTOCOL section 5)."""
    worst = {"p": (-1.0, None), "p_opposite": (-1.0, None)}
    per = {}
    for g in geos_used:
        r = fn([c for c in geos_used if c != g])
        per[g] = dict(beta=r["beta"], p=r["p"])
        for k in worst:
            if r[k] > worst[k][0]:
                worst[k] = (r[k], g)
    return dict(max_p=worst["p"][0], max_p_left_out=worst["p"][1], max_p_opposite=worst["p_opposite"][0],
                max_p_opposite_left_out=worst["p_opposite"][1], rests_on_one_country_if_supported=
                (worst["p"][1] if worst["p"][0] > LOO_P else None), per_country=per)


# ---------------------------------------------------------------- E-HF1 (varies D1)

def _lfs_cycle(cy: pd.DataFrame, raw: dict) -> pd.DataFrame:
    """U replaced by lfsa_urgan Y25-74 (citizen TOTAL) for every country: one source, no splice, its own breaks."""
    s, b = build.cell(raw["une_lfs"], age="Y25-74")
    return _put(cy, "U", s, b)


def e_hf1(cy, cl, geos, fstd, raw, B=B, extras=True) -> dict:
    spec = specs.TESTS["D1"]
    cyl = _lfs_cycle(cy, raw)
    ctx = specs.Ctx(cl, fstd)

    def est(gs, with_ci=False, variant="country_trends"):
        return specs.estimate(cyl, cl, spec, ctx, gs, variant=variant, B=B, with_ci=with_ci)

    r = est(geos, with_ci=True)
    out = dict(id="E-HF1", varies="D1", side=-1, family="E",
               what="D1 with country linear trends and lfsa_urgan U for every country, 1997-2025: b2 on log q_{t-1} x F_c",
               **_pick(r), years_used=[min(r["years_used"]), max(r["years_used"])], geos_used=r["geos_used"],
               mde_this_run=r["mde"], explore_reference=EXPLORE_REFERENCE["E-HF1"],
               label="a pass supports D1-with-country-trends only; it never changes D1's verdict and is not by itself "
                     "evidence for the floor mechanism over the income-effect account")
    if not extras:
        return out
    out["leave_one_out"] = _loo(lambda gs: est(gs), r["geos_used"])
    rob = {}
    rob["no_trends_same_frame"] = _pick(est(geos, variant=None))
    # the lead: log q_{t+1} and log q_{t+1} x F added, trends kept; the lagged term's coefficient and the lead's
    fr = specs.frame(cyl, spec, ctx, geos, "lead")
    y, x, Z, g, M = specs.design(fr, spec["fe"], trends=True)
    rl = inf.wcr(y, x, Z, g, side=-1, B=B)
    cols = [c for c in fr["names"] if c != fr["lead"][0]]
    t = (M["year"].to_numpy(float) - 2010) / 10
    Zl = np.column_stack([inf.fe_matrix(M, list(spec["fe"])), M[["x"] + cols].to_numpy(float),
                          specs.break_dummies(M, fr["breaks"])] +
                         [(M["geo"].to_numpy() == gg) * t for gg in sorted(set(M["geo"]))])
    rf = inf.wcr(y, M[fr["lead"][0]].to_numpy(float), Zl, g, side=0, B=B)
    rob["lead"] = dict(lag_given_lead=_pick(rl), lead_x_F=dict(beta=rf["beta"], se=rf["se"], p_two_sided=rf["p"]))
    # the decomposition: log CP041 x F and -log IGD_NNRG x F (both lagged), with both main effects, trends
    h = raw["hicp"]
    comp = {}
    for c in ("CP041", "IGD_NNRG"):
        s, _ = build.cell(h, coicop=c)
        s, _ = build._shift(np.log(s), {}, 1)
        comp[c] = s[~s.index.duplicated()]
    fr = specs.frame(cyl, spec, ctx, geos, None)
    M = fr["M"].copy()
    key = pd.MultiIndex.from_arrays([M["geo"], M["year"]])
    F = M["geo"].map(ctx.F).to_numpy(float)
    rent = comp["CP041"].reindex(key).to_numpy(float)
    goods = -comp["IGD_NNRG"].reindex(key).to_numpy(float)
    base = [inf.fe_matrix(M, list(spec["fe"])), M[[c for c in fr["names"] if c.startswith("c")]].to_numpy(float),
            specs.break_dummies(M, fr["breaks"])] + [(M["geo"].to_numpy() == gg) * ((M["year"].to_numpy(float) - 2010)
                                                                                    / 10) for gg in sorted(set(M["geo"]))]
    yv = M["y"].to_numpy(float)
    ra = inf.wcr(yv, rent * F, np.column_stack(base + [goods * F, rent, goods]), M["geo"].to_numpy(), side=0, B=B)
    rg = inf.wcr(yv, goods * F, np.column_stack(base + [rent * F, rent, goods]), M["geo"].to_numpy(), side=0, B=B)
    rob["decomposition"] = dict(rent_x_F=dict(beta=ra["beta"], se=ra["se"], p_two_sided=ra["p"]),
                                minus_goods_x_F=dict(beta=rg["beta"], se=rg["se"], p_two_sided=rg["p"]))
    rob["frozen_U_with_trends"] = _pick(specs.estimate(cy, cl, spec, ctx, geos, variant="country_trends", B=B,
                                                       with_ci=False))
    out["robustness_no_verdict"] = rob
    return out


# ---------------------------------------------------------------- E-OCC1 (premise of C-4)

def _occ_long(raw: dict, geos, years=(2011, 2019), min_years=5) -> tuple[pd.DataFrame, list]:
    occ = raw["occ"]
    cells, br = {}, []
    for a in ("Y15-24", "Y15-64"):
        for i in ("OC4", "TOTAL"):
            s, b = build.cell(occ, age=a, isco08=i)
            cells[(a, i)] = s
            br.append(b)
    breaks = build._union(*br)
    young = 100 * cells[("Y15-24", "OC4")] / cells[("Y15-24", "TOTAL")]
    prime = 100 * (cells[("Y15-64", "OC4")] - cells[("Y15-24", "OC4")]) / \
        (cells[("Y15-64", "TOTAL")] - cells[("Y15-24", "TOTAL")])
    w = pd.concat([young.rename("young"), prime.rename("prime")], axis=1).dropna().reset_index()
    w = w[w["geo"].isin(geos) & w["year"].between(*years) & ~w["year"].isin(build.DROP_YEARS)]
    keep = w.groupby("geo")["year"].transform("size") >= min_years
    w = w[keep].reset_index(drop=True)
    d = pd.concat([w[["geo", "year"]].assign(s=w["young"], young=1.0),
                   w[["geo", "year"]].assign(s=w["prime"], young=0.0)], ignore_index=True)
    d["cy"] = d["geo"] + "_" + d["year"].astype(str)
    bl = sorted((g, int(t)) for g, ts in breaks.items() for t in ts if years[0] < int(t) <= years[1])
    return d, bl


def _occ_fit(d: pd.DataFrame, bl, gs, B=B, breaks=True, outcome="s") -> dict:
    d = d[d["geo"].isin(gs)].reset_index(drop=True)
    blocks = [inf.fe_matrix(d, "cy")]
    if breaks:
        blocks.append(specs.break_dummies(d, bl) * d["young"].to_numpy()[:, None])
    return inf.wcr(d[outcome].to_numpy(float), d["young"].to_numpy(float), np.column_stack(blocks),
                   d["geo"].to_numpy(), side=+1, B=B)


def _sign_flip(v: np.ndarray, side=+1) -> float:
    """Exact sign-flip test of the mean of country means (t statistic), one-sided."""
    v = v[np.isfinite(v)]
    n = len(v)

    def tstat(z):
        return z.mean() / (z.std(ddof=1) / math.sqrt(n))
    t0 = tstat(v)
    cnt = tot = 0
    for signs in itertools.product((1, -1), repeat=n):
        tot += 1
        cnt += side * tstat(v * np.array(signs)) >= side * t0 - 1e-12
    return cnt / tot


def e_occ1(cy, cl, geos, fstd, raw, B=B, extras=True) -> dict:
    d, bl = _occ_long(raw, geos)
    gs = sorted(set(d["geo"]))
    r = _occ_fit(d, bl, gs, B=B)
    means = d.assign(sg=d["s"] * np.where(d["young"] == 1, 1, -1)).groupby(["geo", "year"])["sg"].sum() \
        .groupby(level=0).mean()
    sd = float(means.std(ddof=1))
    out = dict(id="E-OCC1", varies=None, premise_of="C4", side=1, family="E",
               what="clerical (OC4) share of employment at 15-24 minus at 25-64, on average across countries, "
                    "2011-2019, country x year FE, young x C3 breaks",
               **_pick(r), years_used=[int(d["year"].min()), int(d["year"].max())], geos_used=gs,
               countries_dropped_lt5_years=sorted(set(geos) - set(gs)),
               mde_this_run=inf.mde(r["se"], r["G"]),
               mde_country_means=inf.mde(sd / math.sqrt(len(means)), len(means)),
               country_mean_gap=means.round(3).to_dict(),
               break_years_2012_2019=sorted({f"{g}{t}" for g, t in bl if g in gs}),
               explore_reference=EXPLORE_REFERENCE["E-OCC1"],
               label="a mapping check shared with entry-job-ladder accounts; tests the premise of C-4's exposure "
                     "measure, not C-4")
    if not extras:
        return out
    out["leave_one_out"] = _loo(lambda g2: _occ_fit(d, bl, g2, B=B), gs)
    rob = {}
    rob["sign_flip_country_means"] = dict(p=_sign_flip(means.to_numpy(float)), mean=float(means.mean()), sd=sd,
                                          G=int(len(means)))
    dl = d.copy()
    dl["ls"] = np.log(dl["s"])
    rob["log_share"] = _pick(_occ_fit(dl, bl, gs, B=B, outcome="ls"))
    rob["no_break_dummies"] = _pick(_occ_fit(d, bl, gs, B=B, breaks=False))
    d2, bl2 = _occ_long(raw, geos, years=(2022, 2025), min_years=2)
    rob["era_2022_2025"] = _pick(_occ_fit(d2, bl2, sorted(set(d2["geo"])), B=B)) if len(d2) else None
    out["robustness_no_verdict"] = rob
    return out


# ---------------------------------------------------------------- E-SCH1 (varies C-6)

def _u2554_lag(cy, raw, geos) -> pd.DataFrame:
    """U(25-54) under C7's rule (une_rt_a for a country it covers, else lfsa_urgan, whole series, never spliced),
    lagged one year on the full annual grid (2021's U reaches the 2022 row); break years move one year later."""
    s, b = build._by_country(build.cell(raw["une"], age="Y25-54"), build.cell(raw["une_lfs"], age="Y25-54"),
                             sorted(set(cy.index.get_level_values(0))))
    sl, bl = build._shift(s, b, 1)
    sf, bf = build._shift(s, b, -1)
    out = _put(cy, "U2554_l1", sl, bl)
    return _put(out, "U2554_f1", sf, bf)


def e_sch1(cy, cl, geos, fstd, raw, B=B, extras=True) -> dict:
    cy2 = _u2554_lag(cy, raw, geos)
    spec = dict(specs.TESTS["C6"], x="U2554_l1")
    ctx = specs.Ctx(cl, fstd)

    def est(gs, sp=spec, variant=None, with_ci=False):
        return specs.estimate(cy2, cl, sp, ctx, gs, variant=variant, B=B, with_ci=with_ci)

    r = est(geos, with_ci=True)
    out = dict(id="E-SCH1", varies="C6", side=1, family="E",
               what="formal education 20-24 on U(25-54) of the previous year (C7 source rule, lag on the full grid)",
               **_pick(r), years_used=[min(r["years_used"]), max(r["years_used"])], geos_used=r["geos_used"],
               mde_this_run=r["mde"], explore_reference=EXPLORE_REFERENCE["E-SCH1"],
               label="a consistency check shared with human-capital accounts (countercyclical enrolment); it never "
                     "changes C-6's verdict")
    if not extras:
        return out
    out["leave_one_out"] = _loo(lambda gs: est(gs), r["geos_used"])
    rob = {}
    rob["country_trends"] = _pick(est(geos, variant="country_trends"))
    rob["excl_2008_2013"] = _pick(est(geos, variant="excl_2008_2013"))
    rob["with_lead_U2554_f1"] = _pick(est(geos, sp=dict(spec, z=["U2554_f1"])))
    rob["C6_contemporaneous_same_sample"] = _pick(est(geos, sp=dict(spec, x="U2554", z=["U2554_l1"]))) | \
        {"note": "U_t with U_{t-1} held: the horse race"}
    out["robustness_no_verdict"] = rob
    return out


# ---------------------------------------------------------------- the contract

def run(cy, cl, geos, fstd, B=B, extras=True) -> dict:
    """The E-hypotheses on these countries: {id: result}; each result has p, p_opposite (one-sided) and G_star."""
    raw = _raw(geos)
    geos = sorted(geos)
    return {"E-HF1": e_hf1(cy, cl, geos, fstd, raw, B=B, extras=extras),
            "E-OCC1": e_occ1(cy, cl, geos, fstd, raw, B=B, extras=extras),
            "E-SCH1": e_sch1(cy, cl, geos, fstd, raw, B=B, extras=extras)}


def main() -> None:
    sys.path.insert(0, os.path.join(ROOT, "explore"))
    import data  # noqa: E402  (explore half, under the lock)
    cy, cl = data.panel()
    geos = sorted(set(cy.index.get_level_values(0)))
    fstd = specs.f_constants(cl, geos)
    res = run(cy, cl, geos, fstd)
    holm = specs.holm(res)
    for k, r in res.items():
        print(f"  {k:7s} b {r['beta']:+.4f} se {r['se']:.4f} p {r['p']:.4f} p_opp {r['p_opposite']:.4f} n {r['n']} "
              f"G {r['G']} G* {r['G_star']:.1f} mde15 {_mde15(r['se'], r['G']):.3f}  LOO max p "
              f"{r['leave_one_out']['max_p']:.3f} ({r['leave_one_out']['max_p_left_out']})  Holm(explore): {holm[k]}")
        for kk, v in r.get("robustness_no_verdict", {}).items():
            print(f"      {kk}: {json.dumps(specs.clean_json(v), default=str)[:240]}")
    out = dict(what="DRAFT e_specs on the EXPLORE half (not a test of E; reproduces the explore estimates)",
               F_standardisation=dict(mean=fstd[0], sd=fstd[1]), tests=res, holm_explore_for_information=holm,
               mde_15={k: _mde15(r["se"], r["G"]) for k, r in res.items()})
    path = os.path.join(ROOT, "results", "explore_synthesis.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(specs.clean_json(out), f, indent=1, default=str)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
