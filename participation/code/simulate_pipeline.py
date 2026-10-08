# simulate_pipeline.py — the whole pipeline (build.py -> specs.py -> verdicts) end to end on SYNTHETIC data, before any
# value is downloaded. eurostat.get is replaced by a fake that answers only the queries of build.MANIFEST (anything else
# raises), validates each query with eurostat's own query checks and the half's countries, and returns long frames with
# the real schema (geo, year, value, flag + the dataset's dimensions; full grid, NaN where a cell has no value).
#
# The synthetic world (World) is generated from a known process, cell by cell:
#   - the cycle U (25-74) and its 25-54, 15-29 twins; q = log(CP041/IGD_NNRG) with country trends and AR noise;
#   - activity cells (sex x five-year band, nationals and all residents) whose aggregates carry the planted effects:
#     25-29/30-34 cells: b1 Q + b2 Q F + k (Q - m_c)^2; 55-64 cells: (b1 - c2) Q; women 35-54: bF Q, men 35-54: bM Q,
#     with bF, bM solved so that A_W(25-54) has slope c3b and A_W - A_M slope c3a (Q = log q_{t-1}, F = standardised
#     floor availability computed from the synthetic coresidence series exactly as build.py does);
#   - employment cells with c4 X_c 1[year >= 2023] in the 20-24 cells; coresidence with slope c1 on Q; formal education
#     with slope c6 on U 25-54; the routine-share change with slope c5 on predicted aging (from a synthetic 2011 age
#     structure); house prices, compensation, tenure and student coresidence as plain noise;
#   - every cell has country and year effects, AR(1) noise, and level shifts at its break events, which carry a 'b'
#     flag (LFS: 2005 in 60% of countries, 2021 in 90%, three more at random; occupation 2011 everywhere; SILC four at
#     random); 0.5% of cells are flagged u and 0.2% c with their values left in (build must blank them), 0.3% are
#     missing, 3% carry harmless flags (p, e, d); coverage starts and ends by country as in docs/data_inventory.md (UK to
#     2019, HR late, CH in prc_hpi_a in I25 only, no Greece in prc_hpi_a, no UK in une_rt_a, no Croatia in
#     nama_10_lp_ulc). The UK gets activity values for 2020-2025 that the build must drop (C1).
# Runs:
#   (1) full runs at production settings (B = R = 9999, intervals, secondaries, robustness) on all 31 countries:
#       null (every planted effect zero), planted, and opposite (D1's and D2's terms reversed);
#   (2) one run on the explore half (16 countries), checking the queries ask only for explore countries;
#   (3) replications (B = R = 999, primary tests only): N_NULL null worlds (rejection rates at 5%, the rate of a false
#       verdict per family, the rate of a model verdict other than inconclusive) and N_PLANT planted worlds (the rate at
#       which each primary test is supported and the model verdict 'favours the model'); both record G* per test and
#       how often it falls below 8 (reported only; the verdicts' qualifier is the leave-one-country-out run, which the
#       full runs (1) and (2) carry and the replications skip for time).
#
# Run from participation/:  ../venv/Scripts/python.exe code/simulate_pipeline.py
# Out: results/simulate_pipeline.json

from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402
import eurostat as es  # noqa: E402
import specs  # noqa: E402

SEED = 20261008
N_NULL, N_PLANT = 200, 40
LAT = np.arange(1994, 2027)                  # latent years
NULL = dict(b1=0.0, b2=0.0, k=0.0, c1=0.0, c2=0.0, c3a=0.0, c3b=0.0, c4=0.0, c5=0.0, c6=0.0)
PLANT = dict(b1=3.0, b2=-6.0, k=-60.0, c1=10.0, c2=10.0, c3a=6.0, c3b=8.0, c4=-0.8, c5=-60.0, c6=1.0)
OPPOSITE = {**PLANT, "b2": 6.0, "k": 60.0}
PLANTED_COEF = {"D1": "b2", "D2": "k", "C1": "c1", "C2": "c2", "C3a": "c3a", "C3b": "c3b", "C4": "c4",
                "C5": "c5", "C6": "c6"}
STRATUM = {c: s for s, cs in es.STRATA.items() for c in cs}
C = list(es.COUNTRIES)
GI = {c: i for i, c in enumerate(C)}
SPLIT = json.load(open(os.path.join(ROOT, "data", "split.json"), encoding="utf-8"))

# first year of coverage (docs/data_inventory.md, approximately); default given per dataset
LFS_START = {"HU": 1996, "SI": 1996, "CH": 1996, "CZ": 1997, "EE": 1997, "PL": 1997, "RO": 1997, "LT": 1998,
             "LV": 1998, "SK": 1998, "CY": 1999, "BG": 2000, "MT": 2000, "HR": 2002}
HICP_START = {"HR": 1998, "CZ": 2000, "SI": 2000, "HU": 2001, "RO": 2001, "CH": 2005}
SILC_START = {"HR": 2010, "RO": 2007, "BG": 2006, "MT": 2005, "CH": 2007, "DE": 2005, "UK": 2005}


def yi(y):
    return int(y) - int(LAT[0])


def ar1(rng, shape, rho, sd):
    x = np.zeros(shape)
    x[..., 0] = rng.normal(0, sd / math.sqrt(1 - rho * rho), shape[:-1])
    for j in range(1, shape[-1]):
        x[..., j] = rho * x[..., j - 1] + rng.normal(0, sd, shape[:-1])
    return x


class World:
    """One synthetic world: long frames for every manifest query, all 31 countries."""

    def __init__(self, seed: int, plant: dict, run_geos):
        self.plant, self.r = dict(plant), np.random.default_rng(seed)
        r, G, Y = self.r, len(C), len(LAT)
        self.run_geos = sorted(run_geos)
        base_u = {"Nordic": 6, "Continental": 6, "Anglo": 7, "South": 11, "CEE": 9}
        u0 = np.array([base_u[STRATUM[c]] for c in C]) + r.normal(0, 1.5, G)
        cyc = ar1(r, (G, Y), 0.8, 1.0)
        common = r.normal(0, 0.3, Y)
        common[yi(2009):yi(2014)] += [1.5, 2.5, 2.5, 3.0, 2.5]
        self.U = np.clip(u0[:, None] + 1.2 * cyc + common, 1.5, None)
        self.Udev = self.U - self.U.mean(1, keepdims=True)
        self.U2554 = self.U + 0.4 + r.normal(0, 0.2, (G, Y))
        self.U1529 = 1.8 * self.U + r.normal(0, 0.8, (G, Y))
        a, tr = r.normal(0, 0.2, G), r.normal(0.15, 0.08, G)
        logq = (a[:, None] + tr[:, None] * (LAT - 2010) / 10 + np.cumsum(r.normal(0, 0.01, Y))
                + ar1(r, (G, Y), 0.85, 0.025) - 0.01 * cyc)
        self.logq = logq
        self.Q = np.full((G, Y), np.nan)
        self.Q[:, 1:] = logq[:, :-1]
        # break events
        self.ev_lfs = np.zeros((G, Y), bool)
        self.ev_lfs[:, yi(2005)] = r.random(G) < 0.6
        self.ev_lfs[:, yi(2021)] = r.random(G) < 0.9
        for _ in range(3):
            self.ev_lfs[r.integers(G), yi(r.integers(1998, 2019))] = True
        self.ev_occ = self.ev_lfs.copy()
        self.ev_occ[:, yi(2011)] = True
        self.ev_silc = np.zeros((G, Y), bool)
        for _ in range(4):
            self.ev_silc[r.integers(G), yi(r.integers(2006, 2024))] = True
        self.ev_hicp = np.zeros((G, Y), bool)
        for _ in range(2):
            self.ev_hicp[r.integers(G), yi(r.integers(1999, 2024))] = True
        self.frames = {}
        self._build()

    # ------------------------------------------------ helpers
    def cov(self, start: dict, default: int, end: int = 2025, uk_end: int = 2019, ends: dict | None = None):
        m = np.zeros((len(C), len(LAT)), bool)
        for i, c in enumerate(C):
            lo = start.get(c, default)
            hi = uk_end if c == "UK" else (ends or {}).get(c, end)
            m[i, yi(lo):yi(hi) + 1] = True
        return m

    def series(self, systematic, events, level, shift_sd=1.0, noise=0.8, rho=0.5):
        """systematic (G,Y) + country level + year effect + level shifts at the events + AR(1) noise."""
        r, G, Y = self.r, len(C), len(LAT)
        yeff = np.cumsum(r.normal(0, 0.3, Y))
        shifts = np.cumsum(events * r.normal(0, shift_sd, (G, Y)), axis=1)
        lv = np.broadcast_to(np.asarray(level, float), (G,))[:, None]
        return systematic + lv + yeff + shifts + ar1(r, (G, Y), rho, noise)

    def flags(self, events, cover, missing=0.003, u=0.005, c=0.002):
        r, G, Y = self.r, len(C), len(LAT)
        f = np.full((G, Y), "", dtype=object)
        x = r.random((G, Y))
        f[x < 0.03] = r.choice(["p", "e", "d"], size=int((x < 0.03).sum()))
        f[events] = "b"
        uu = r.random((G, Y)) < u
        f[uu] = np.where(events[uu], "bu", "u")
        f[r.random((G, Y)) < c] = "c"
        miss = (r.random((G, Y)) < missing) | ~cover
        f[~cover] = ""
        return f, miss

    def emit(self, mid: str, cells: dict, years=(1995, 2025), drop_geos=()):
        """cells: {combo tuple of (dim, code): (values (G,Y), events (G,Y), cover (G,Y))} -> long frame."""
        lo, hi = years
        yrs = np.arange(lo, hi + 1)
        cols = [k for k, _ in next(iter(cells))]
        parts = []
        for combo, (val, ev, cover) in cells.items():
            fl, miss = self.flags(ev, cover)
            v = np.where(miss, np.nan, val)[:, yi(lo):yi(hi) + 1]
            fl = fl[:, yi(lo):yi(hi) + 1]
            d = pd.DataFrame({"geo": np.repeat(C, len(yrs)), "year": np.tile(yrs, len(C)),
                              "value": v.ravel(), "flag": fl.ravel().astype(str)})
            for k, code in combo:
                d[k] = code
            parts.append(d)
        df = pd.concat(parts, ignore_index=True)
        df = df[~df["geo"].isin(drop_geos)]
        has = df.groupby("geo")["value"].transform(lambda s: s.notna().any())
        self.frames[mid] = df[has.astype(bool)][["geo", "year", "value", "flag"] + cols].reset_index(drop=True)

    # ------------------------------------------------ the datasets
    def _build(self):
        r, p, G, Y = self.r, self.plant, len(C), len(LAT)
        lfs = self.cov(LFS_START, 1995)
        # coresidence first: F is computed from it as build.py does
        Fbase = np.array([{"Nordic": 12, "Continental": 25, "Anglo": 25, "South": 55, "CEE": 55}[STRATUM[c]]
                          for c in C]) + r.normal(0, 5, G)
        silc = self.cov(SILC_START, 2004, ends={"IS": 2020}, uk_end=2018)
        cores = self.series(p["c1"] * self.Q + 0.3 * self.Udev, self.ev_silc, Fbase, noise=0.8)
        self.emit("cores", {(("age", "Y25-34"), ("sex", "T"), ("unit", "PC")): (cores, self.ev_silc, silc)},
                  years=(2003, 2025))
        cf = build.cell(self.frames["cores"])[0]
        Fraw = {g: build.first_three(cf.xs(g, level=0) if g in set(cf.index.get_level_values(0))
                                     else pd.Series(dtype=float))[0] for g in C}
        fr = np.array([Fraw[g] for g in self.run_geos], float)
        fr = fr[np.isfinite(fr)]
        self.fstd = (float(fr.mean()), float(fr.std()))
        F = np.array([(Fraw[g] - self.fstd[0]) / self.fstd[1] if np.isfinite(Fraw[g]) else 0.0 for g in C])
        self.F = F
        # activity: D1, D2, C2, C3
        Q = np.nan_to_num(self.Q)
        win = lfs & (LAT >= 1997)[None, :] & ~np.isin(LAT, (2020, 2021))[None, :]
        m = np.array([Q[i, win[i]].mean() if win[i].any() else 0.0 for i in range(G)])
        sq = (Q - m[:, None]) ** 2
        young = p["b1"] * Q + p["b2"] * Q * F[:, None] + p["k"] * sq
        old = (p["b1"] - p["c2"]) * Q
        bF = (6 * p["c3b"] - 2 * p["b1"]) / 4
        bM = (6 * (p["c3b"] - p["c3a"]) - 2 * p["b1"]) / 4
        lfs_uk = lfs.copy()
        lfs_uk[GI["UK"], yi(2020):yi(2025) + 1] = True        # values the build must drop (C1)
        cells, emp = {}, {}
        for s in "MF":
            for a in build.AGES_PRIME + build.AGES_OLD:
                if a in ("Y25-29", "Y30-34"):
                    sysm, lv = young, (88 if s == "M" else 78)
                elif a in build.AGES_OLD:
                    sysm, lv = old, (60 if s == "M" else 48)
                else:
                    sysm, lv = (bF if s == "F" else bM) * Q, (92 if s == "M" else 80)
                nat = self.series(sysm - 0.4 * self.Udev, self.ev_lfs, lv + r.normal(0, 3, G))
                tot = nat + r.normal(0, 1, G)[:, None] + r.normal(0, 0.3, (G, Y))
                cells[(("unit", "PC"), ("sex", s), ("age", a), ("citizen", "NAT"))] = (nat, self.ev_lfs, lfs_uk)
                cells[(("unit", "PC"), ("sex", s), ("age", a), ("citizen", "TOTAL"))] = (tot, self.ev_lfs, lfs_uk)
        self.emit("act", cells)
        # employment: C-4
        X = 8 + 12 * r.random(G)                                  # exposure, points (uniform)
        self.X_true = X
        post = (LAT >= 2023)[None, :].astype(float)
        for s in "MF":
            for a in ["Y20-24"] + build.AGES_PRIME:
                sysm = (p["c4"] * X[:, None] * post if a == "Y20-24" else 0.0) - (1.0 if a == "Y20-24" else 0.6) * self.Udev
                nat = self.series(sysm + np.zeros((G, Y)), self.ev_lfs, (50 if a == "Y20-24" else 78) + r.normal(0, 4, G),
                                  noise=0.6)
                tot = nat + r.normal(0, 1, G)[:, None] + r.normal(0, 0.3, (G, Y))
                emp[(("unit", "PC"), ("sex", s), ("age", a), ("citizen", "NAT"))] = (nat, self.ev_lfs, lfs)
                emp[(("unit", "PC"), ("sex", s), ("age", a), ("citizen", "TOTAL"))] = (tot, self.ev_lfs, lfs)
        self.emit("emp", emp)
        # unemployment
        ages = {"Y25-74": self.U, "Y25-54": self.U2554, "Y15-29": self.U1529}
        self.emit("une", {(("age", a), ("unit", "PC_ACT"), ("sex", "T")): (v, self.ev_lfs, lfs) for a, v in ages.items()},
                  drop_geos=("UK",))
        self.emit("une_lfs", {(("unit", "PC"), ("sex", "T"), ("age", a), ("citizen", "TOTAL")):
                              (v + r.normal(0, 0.15, (G, Y)), self.ev_lfs, lfs) for a, v in ages.items()})
        # prices
        hc = self.cov(HICP_START, 1996)
        g = np.cumsum(0.015 + r.normal(0, 0.01, (G, Y)), axis=1)
        nnrg = 100 * np.exp(g)
        cp041 = 100 * np.exp(g + self.logq)
        cp00 = 100 * np.exp(0.9 * g + 0.3 * self.logq + r.normal(0, 0.005, (G, Y)))
        self.emit("hicp", {(("unit", "INX_A_AVG"), ("coicop", k)): (v, self.ev_hicp, hc)
                           for k, v in (("CP041", cp041), ("IGD_NNRG", nnrg), ("CP00", cp00))}, years=(1996, 2025))
        hpi = 100 * np.exp(g + 1.5 * self.logq + ar1(r, (G, Y), 0.9, 0.04))
        noev = np.zeros((G, Y), bool)
        hcov = self.cov({c: 2005 + int(r.integers(0, 6)) for c in C}, 2005)
        i15 = hcov.copy()
        i15[GI["CH"]] = False
        self.emit("hpi", {(("purchase", "TOTAL"), ("unit", "I15_A_AVG")): (hpi, noev, i15),
                          (("purchase", "TOTAL"), ("unit", "I25_A_AVG")): (hpi * 0.8, noev, hcov)},
                  years=(2005, 2025), drop_geos=("EL",))
        self.emit("hpi_el", {(("unit", "I15_A_AVG"),): (hpi, noev, self.cov({}, 2000))}, years=(2000, 2025))
        self.emit("comp", {(("unit", "NAC"), ("na_item", "D1_SAL_PER")): (30000 * np.exp(g + r.normal(0, 0.01, (G, Y))),
                                                                          noev, lfs)}, drop_geos=("HR",))
        # SILC moderators
        self.emit("tenure", {(("tenure", "OWN_NL"), ("sex", "T"), ("age", "Y55-64"), ("unit", "PC")):
                             (self.series(np.zeros((G, Y)), noev, 20 + 60 * r.random(G), noise=1.0), noev,
                              self.cov({}, 2015, uk_end=2018))}, years=(2015, 2025))
        self.emit("stud", {(("wstatus", "EDUC"), ("age", "Y18-24"), ("unit", "PC")):
                           (np.clip(self.series(np.zeros((G, Y)), noev, 40 + 55 * r.random(G), noise=1.0), 1, 99),
                            noev, silc)}, years=(2003, 2025))
        # education: C-6
        educ = self.series(p["c6"] * (self.U2554 - self.U2554.mean(1, keepdims=True)), self.ev_lfs,
                           30 + 30 * r.random(G), noise=0.8)
        self.emit("educ", {(("sex", "T"), ("age", "Y20-24"), ("wstatus", "POP"), ("training", "FE"), ("unit", "PC")):
                           (educ, self.ev_lfs, self.cov({}, 2004))}, years=(2004, 2025))
        # population 2011 and predicted aging: C-5
        ages_n = np.array([100 if a == "Y_OPEN" else int(a[1:]) for a in build.AGES_POP])
        lam, th, sh = r.uniform(0.0, 0.8, G), r.uniform(0.0, 0.6, G), r.uniform(-8, 8, G)
        surv = np.where(ages_n > 70, np.exp(-((ages_n - 70) / 14.0) ** 2), 1.0)
        size = np.array([1e6 * (1 + 50 * r.random()) for _ in C])
        pop11 = size[:, None] * np.exp(-lam[:, None] * (ages_n - 13) / 50) \
            * (1 + th[:, None] * np.exp(-((ages_n - 50 - sh[:, None]) / 8.0) ** 2)) * surv
        tot = lambda P, lo, hi=999: P[:, (ages_n >= lo) & (ages_n <= hi)].sum(1)  # noqa: E731
        self.aging = tot(pop11, 48) / tot(pop11, 13, 47) - tot(pop11, 56) / tot(pop11, 21, 55)
        popc = {}
        for j, a in enumerate(build.AGES_POP):
            v = np.repeat(pop11[:, j:j + 1], len(LAT), axis=1) * (1 + 0.01 * r.normal(0, 1, (G, Y)))
            v[:, yi(2011)] = pop11[:, j]                          # the 2011 structure is the one aging is planted on
            popc[(("unit", "NR"), ("age", a), ("sex", "T"))] = (v, noev, self.cov({}, 2011))
        self.emit_pop(popc)
        # occupations: C-4 exposure and C-5 routine change
        stoff = {"Nordic": -1.0, "Continental": 0.0, "Anglo": 0.5, "South": 1.0, "CEE": 1.5}
        dr = np.array([stoff[STRATUM[c]] for c in C]) + p["c5"] * (self.aging - self.aging.mean()) + r.normal(0, 1.0, G)
        self.routine_true = dr
        r0 = 25 + 15 * r.random(G)
        share = r0[:, None] + dr[:, None] * np.clip((LAT - 2011) / 8, 0, None) + r.normal(0, 0.3, (G, Y))
        share[:, yi(2011)], share[:, yi(2019)] = r0, r0 + dr
        tot64 = (500 + 20000 * r.random(G))[:, None] * np.exp(r.normal(0, 0.01, (G, Y)))
        w = r.dirichlet([4, 4, 4], size=(G, Y))
        tot24 = (50 + 2000 * r.random(G))[:, None] * np.exp(r.normal(0, 0.02, (G, Y)))
        xs = X[:, None] + r.normal(0, 0.4, (G, Y))
        young_occ = {"OC4": tot24 * xs / 100, "OC7": tot24 * 0.10, "OC8": tot24 * 0.08, "TOTAL": tot24}
        all_occ = {"OC4": tot64 * share / 100 * w[..., 0], "OC7": tot64 * share / 100 * w[..., 1],
                   "OC8": tot64 * share / 100 * w[..., 2], "TOTAL": tot64}
        occ = {}
        for age, vals in (("Y15-24", young_occ), ("Y15-64", all_occ)):
            for k, v in vals.items():
                occ[(("unit", "THS_PER"), ("sex", "T"), ("age", age), ("wstatus", "EMP"), ("isco08", k))] = \
                    (v, self.ev_occ, lfs)
        self.emit_occ(occ)

    def emit_pop(self, cells):
        """Population: no u/c flags or missing cells in 2011 (an age structure with a hole has no aging measure)."""
        lo, hi = 2011, 2025
        yrs = np.arange(lo, hi + 1)
        parts = []
        for combo, (val, _, _) in cells.items():
            d = pd.DataFrame({"geo": np.repeat(C, len(yrs)), "year": np.tile(yrs, len(C)),
                              "value": val[:, yi(lo):yi(hi) + 1].ravel(), "flag": ""})
            for k, code in combo:
                d[k] = code
            parts.append(d)
        self.frames["pop"] = pd.concat(parts, ignore_index=True)

    def emit_occ(self, cells):
        """Occupations: the generic flags, but no missing or unreliable cells at 15-64 in 2011 and 2019, so the
        planted change is observed (the 15-24 exposure cells keep theirs: X_c falls back to one year)."""
        self.emit("occ", cells)
        d = self.frames["occ"]
        fix = (d["age"] == "Y15-64") & d["year"].isin([2011, 2019])
        if fix.any():
            truth = {}
            for combo, (val, _, _) in cells.items():
                cd = dict(combo)
                if cd["age"] == "Y15-64":
                    truth[cd["isco08"]] = val
            sub = d[fix]
            d.loc[fix, "value"] = [truth[i][GI[g], yi(y)] for g, y, i in zip(sub["geo"], sub["year"], sub["isco08"])]
            d.loc[fix, "flag"] = np.where(sub["flag"].str.contains("b"), "b", "")
        self.frames["occ"] = d


# ---------------------------------------------------------------- the fake loader

class Fake:
    """Stands in for eurostat.get: manifest queries only, the half's countries only."""

    def __init__(self, world: World):
        self.world, self.calls = world, []
        self.canon = {}
        for m in build.MANIFEST:
            code, filters, _, since = es._check_query(m["dataset"], m["filters"], ["AT"], m.get("since"))
            self.canon[(code, json.dumps(filters, sort_keys=True), since)] = m["id"]

    def __call__(self, code, filters, geos, half, since=None):
        code, f, geos, since = es._check_query(code, filters, geos, since)
        if half not in ("explore", "confirm"):
            raise es.BlindingError(f"synthetic loader: half {half!r}")
        allowed = set(SPLIT["explore"]) if half == "explore" else set(es.COUNTRIES)
        if not geos or set(geos) - allowed:
            raise es.BlindingError(f"synthetic loader: {sorted(set(geos) - allowed)} outside half {half}")
        key = (code, json.dumps(f, sort_keys=True), since)
        if key not in self.canon:
            raise KeyError(f"query outside the manifest: {key}")
        mid = self.canon[key]
        expect = build.query_geos(build.BY_ID[mid], build.geos_for(half))
        if sorted(expect) != geos:
            raise ValueError(f"{mid}: asked for {geos}, the half's query is {sorted(expect)}")
        self.calls.append(dict(id=mid, dataset=code, half=half, geos=geos))
        df = self.world.frames[mid]
        return df[df["geo"].isin(geos)].reset_index(drop=True).copy()


def with_world(world: World, half: str):
    """(cy, cl, fake) built through build.py with eurostat.get replaced by the fake for this world."""
    fake, real = Fake(world), es.get
    build.reset()
    es.get = fake
    try:
        cy, cl = build.country_year(half), build.country_level(half)
    finally:
        es.get = real
        build.reset()
    return cy, cl, fake


def summary(res: dict) -> dict:
    keys = ("beta", "se", "p", "p_opposite", "G_star", "n", "G", "ci", "mde")
    return {"verdicts": res["verdicts"], "model_verdict": res["model_verdict"], "qualifiers": res["qualifiers"],
            "model_qualifier": res["model_qualifier"], "leave_one_out": res["leave_one_out"],
            "tests": {k: {kk: v.get(kk) for kk in keys} for k, v in res["tests"].items()}}


def main() -> None:
    t0 = time.time()
    out = {"plant": PLANT, "opposite": OPPOSITE, "planted_coefficient": PLANTED_COEF, "seed": SEED}
    # (1) full runs
    for name, plant, seed in (("null", NULL, SEED), ("planted", PLANT, SEED + 1), ("opposite", OPPOSITE, SEED + 2)):
        w = World(seed, plant, C)
        cy, cl, fake = with_world(w, "confirm")
        res = specs.run("confirm", cy, cl)
        s = summary(res)
        s["secondary"] = {k: {kk: v.get(kk) for kk in ("beta", "se", "p", "p_opposite", "ci", "G_star",
                                                       "pre_trend_flag", "joint_pre_p")}
                          for k, v in res["secondary"].items()}
        s["robustness"] = {k: ({kk: v.get(kk) for kk in ("beta", "se", "p", "n", "G")} if "error" not in v else v)
                           for k, v in res["robustness"].items()}
        s["F_standardisation"] = res["F_standardisation"]
        s["dgp_F_standardisation"] = list(w.fstd)
        s["queries"] = sorted({c["id"] for c in fake.calls})
        s["n_queries"] = len(fake.calls)
        s["panel"] = {"years": sorted(int(y) for y in set(cy.index.get_level_values(1))),
                      "uk_max_year": int(cy.xs("UK", level=0).index.max()),
                      "uk_activity_after_2019_in_raw": bool(((w.frames["act"]["geo"] == "UK")
                                                             & (w.frames["act"]["year"] > 2019)
                                                             & w.frames["act"]["value"].notna()).any()),
                      "years_used": {k: v.get("years_used") for k, v in res["tests"].items()},
                      "geos_used": {k: v.get("geos_used") for k, v in res["tests"].items()}}
        out[f"full_{name}"] = s
        print(f"full {name}: {s['verdicts']} -> {s['model_verdict']} ({time.time() - t0:.0f}s)")
        for k in specs.PRIMARY + ["C3a", "C3b"]:
            r = s["tests"][k]
            print(f"   {k:4s} beta {r['beta'] if r['beta'] is None else round(r['beta'], 3)} p {r['p']:.4f} "
                  f"p_opp {r['p_opposite']:.4f} G* {r['G_star']:.1f}")
    # (2) the explore half
    w = World(SEED + 3, PLANT, SPLIT["explore"])
    cy, cl, fake = with_world(w, "explore")
    res = specs.run("explore", cy, cl, B=999, R=999, robustness=False)
    out["explore_run"] = {**summary(res), "geos": res["geos"],
                          "query_geos_within_explore": all(set(c["geos"]) <= set(SPLIT["explore"]) for c in fake.calls),
                          "queries": sorted({c["id"] for c in fake.calls}), "n_queries": len(fake.calls)}
    print(f"explore run: {res['verdicts']} ({time.time() - t0:.0f}s)")
    # (3) replications
    for name, plant, n, base in (("null", NULL, N_NULL, 1000), ("planted", PLANT, N_PLANT, 5000)):
        rej, sup, fam, model, gs = {}, {}, {"D": 0, "C": 0}, {}, {}
        for i in range(n):
            w = World(SEED + base + i, plant, C)
            cy, cl, _ = with_world(w, "confirm")
            res = specs.run("confirm", cy, cl, B=999, R=999, with_ci=False, secondary=False, robustness=False,
                            loo=False)
            for k, r in res["tests"].items():
                rej[k] = rej.get(k, 0) + (r["p"] <= 0.05)
                rej[k + "_opposite"] = rej.get(k + "_opposite", 0) + (r["p_opposite"] <= 0.05)
                gs.setdefault(k, []).append(r["G_star"])
            for k, lab in res["verdicts"].items():
                sup[(k, lab)] = sup.get((k, lab), 0) + 1
            for f, ids in specs.FAMILIES.items():
                fam[f] += any(res["verdicts"][k] in ("supported", "contradicted") for k in ids)
            model[res["model_verdict"]] = model.get(res["model_verdict"], 0) + 1
        out[f"reps_{name}"] = {"n": n, "reject_5pct": {k: v / n for k, v in rej.items()},
                               "labels": {f"{k}|{lab}": v / n for (k, lab), v in sorted(sup.items())},
                               "family_any_verdict": {f: v / n for f, v in fam.items()},
                               "model_verdict": {k: v / n for k, v in model.items()},
                               "G_star_mean": {k: float(np.mean(v)) for k, v in gs.items()},
                               "G_star_below_8": {k: float(np.mean(np.array(v) < 8))
                                                  for k, v in gs.items()}}
        print(f"reps {name}: {out[f'reps_{name}']['family_any_verdict']} {out[f'reps_{name}']['model_verdict']} "
              f"({time.time() - t0:.0f}s)")
    out["seconds"] = round(time.time() - t0, 1)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    path = os.path.join(ROOT, "results", "simulate_pipeline.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(specs.clean_json(out), f, indent=1)
    print(f"wrote {path} ({out['seconds']}s)")


if __name__ == "__main__":
    main()
