# us_study.py — the US deep study of longrun/PROTOCOL.md section 6: one country, 1948-2025, NO verdict. Run once,
# first, after the L-freeze tag (the US is in the explore half by rule); its output is committed as it comes out,
# before any free exploration of US data.
#
# Series (all through fetch.py's US doors, logged):
#   participation  CPS civilian rates, not seasonally adjusted, annual means of monthly values (2025: the months
#                  published): 25-34 men LNU01300164, women LNU01300327; 20-24 LNU01300037, LNU01300038; 55-64
#                  LNU01300190, LNU01300347 (DBnomics mirror BLS/ln; the log records the mirror's index date);
#   cycle          LNU04000060, unemployment rate 25-54, NSA, annual mean;
#   q_US           log(DTENRG / DGDSRG) of year t-1 (BEA NIPA T2.4.4 annual, DBnomics BEA/NIPA-T20404);
#   coresidence    Census AD-3 (25-34), 'child of householder', men, women and their equal-weight mean, 1967 to
#                  AD-3's last year; AD-1 from the first year after AD-3's last year, as a new segment; AD-1's census
#                  points (1960, 1970, 1980) a separate segment (their own dummy), kept beside AD-3's values for the
#                  same years and never overwriting them (rows ordered by year, then series);
#   enrolment      Census CPS October Table A-2 (hst_enroll02.xlsx), both sexes; 20-24 = (2 x the 20-21 rate + 3 x the
#                  22-24 rate) / 5.
# Segments: data/segments.csv series us_cps (participation, cycle), us_coresid, us_enrol, us_q, plus the AD-3/AD-1
# seams above, as dummies. q_US's terciles lie inside its longest us_q segment by section 5's rule (q_segment).
# Analyses (each in levels with the cycle and the segment dummies, and in non-overlapping five-year differences within
# segments, every analysis; Newey-West standard errors, Bartlett kernel, 4 lags in both; men, women and their mean
# where the series allow: participation and coresidence by sex, enrolment both sexes only):
#   U-K2  the piecewise basis on the US's own q_US terciles within q_US's longest segment (section 5's rule): g3 - g1, g3
#   U-Y0  g1
#   U-C1  coresidence on q_US, with the cycle
#   U-S   enrolment 20-24 on the cycle
# The Census tables' layouts are read by the parsers below without having been opened (no value was seen before the
# freeze); a parser that cannot find its columns raises, and its fix is plumbing (section 8).
#
# Run from longrun/ after the L-freeze:  ../../venv/Scripts/python.exe code/us_study.py
# Out: results/us_study.json

from __future__ import annotations

import io
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fetch  # noqa: E402
import inference_l as infl  # noqa: E402
import segments as sg  # noqa: E402
import specs  # noqa: E402

OUT = os.path.join(LROOT, "results", "us_study.json")
PART = {"M2534": "LNU01300164", "F2534": "LNU01300327", "M2024": "LNU01300037", "F2024": "LNU01300038",
        "M5564": "LNU01300190", "F5564": "LNU01300347"}
CYCLE = "LNU04000060"
BEA = {"tenant_rent": "DTENRG-A", "goods": "DGDSRG-A"}
NW_LAGS = 4
FIRST, LAST = 1948, 2025


def annual_mean(df: pd.DataFrame) -> pd.Series:
    """Annual means of monthly values (every month published in the year)."""
    d = df.copy()
    d["year"] = d["period"].astype(str).str[:4].astype(int)
    return d.dropna(subset=["value"]).groupby("year")["value"].mean()


def fetch_series(half: str = "explore") -> tuple[pd.DataFrame, dict]:
    meta = {}
    cols = {}
    for k, s in {**PART, "U": CYCLE}.items():
        df = fetch.dbnomics(f"BLS/ln/{s}", half)
        cols[k] = annual_mean(df)
        meta[s] = df.attrs.get("indexed_at")
    bea = {}
    for k, s in BEA.items():
        df = fetch.dbnomics(f"BEA/NIPA-T20404/{s}", half)
        bea[k] = pd.Series(df["value"].to_numpy(float), index=df["period"].astype(str).str[:4].astype(int))
        meta[s] = df.attrs.get("indexed_at")
    q = np.log(bea["tenant_rent"] / bea["goods"])
    d = pd.DataFrame(cols).reindex(range(FIRST, LAST + 1))
    d["logq_l1"] = q.reindex(range(FIRST - 1, LAST)).to_numpy(float)
    return d, meta


def _year_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Rows whose first cell is a year (an optional footnote mark allowed); the year as index."""
    first = df.iloc[:, 0].astype(str).str.strip()
    yr = first.str.extract(r"^(\d{4})")[0]
    keep = yr.notna()
    out = df[keep].copy()
    out.index = yr[keep].astype(int).to_numpy()
    out.attrs["labels"] = first[keep].tolist()
    return out


def coresidence(half: str = "explore") -> pd.DataFrame:
    """Percent of 25-34 living as child of the householder (men, women, their equal-weight mean), one row per (year,
    series): 'AD-3' (1967 to AD-3's last year), 'AD-1 forward' (AD-1 from the first year after AD-3's last year, a new
    segment) and 'AD-1 census' (AD-1's census points 1960, 1970, 1980: their own segment, kept beside AD-3's values for
    the same years, never overwriting them)."""
    ad3 = pd.read_excel(io.BytesIO(fetch.census_us("ad3_25_34", half)), header=None)
    ad1 = pd.read_excel(io.BytesIO(fetch.census_us("ad1", half)), header=None)
    rows3 = _year_rows(ad3)
    rows1 = _year_rows(ad1)
    if rows3.empty or rows1.empty:
        raise ValueError("Census AD tables: no year rows found; the parser needs fixing (plumbing)")

    # The percent columns of 'child of householder' for men and women are located by header text; the table layout is
    # checked here, not assumed: two percent columns are required (the first is men's, the second women's).
    def pct_cols(df):
        head = df.head(12).astype(str).apply(lambda c: c.str.lower())
        return [j for j in range(df.shape[1]) if head.iloc[:, j].str.contains("child").any()]
    c3, c1 = pct_cols(ad3), pct_cols(ad1)
    if len(c3) < 2 or len(c1) < 2:
        raise ValueError("Census AD tables: could not locate the men's and women's child-of-householder columns")

    def sexes(rows, cols):
        d = rows.iloc[:, cols[:2]].apply(pd.to_numeric, errors="coerce")
        d.columns = ["men", "women"]
        d["both"] = d[["men", "women"]].mean(axis=1, skipna=False)
        return d[~d.index.duplicated(keep="last")]
    s3, s1 = sexes(rows3, c3), sexes(rows1, c1)
    last3 = int(s3["both"].dropna().index.max())
    parts = [s3.assign(series="AD-3"),
             s1[s1.index > last3].assign(series="AD-1 forward"),
             s1[s1.index.isin([1960, 1970, 1980])].assign(series="AD-1 census")]
    out = pd.concat(parts)
    out.index.name = "year"
    return out.reset_index().sort_values(["year", "series"]).reset_index(drop=True)


def enrolment(half: str = "explore") -> pd.Series:
    df = pd.read_excel(io.BytesIO(fetch.census_us("enroll02", half)), header=None)
    head = df.head(15).astype(str).apply(lambda c: c.str.lower())
    c2021 = [j for j in range(df.shape[1]) if head.iloc[:, j].str.contains("20 and 21|20-21|20 to 21").any()]
    c2224 = [j for j in range(df.shape[1]) if head.iloc[:, j].str.contains("22 to 24|22-24").any()]
    if not c2021 or not c2224:
        raise ValueError("hst_enroll02: could not locate the 20-21 and 22-24 columns (plumbing)")
    rows = _year_rows(df)
    a = pd.to_numeric(rows.iloc[:, c2021[0]], errors="coerce")
    b = pd.to_numeric(rows.iloc[:, c2224[0]], errors="coerce")
    s = (2 * a + 3 * b) / 5
    return s[~s.index.duplicated(keep="last")]


def dummies(years: np.ndarray, starts) -> np.ndarray:
    cols = [(years >= t).astype(float) for t in sorted(set(starts)) if years.min() < t <= years.max()]
    return np.column_stack(cols) if cols else np.zeros((len(years), 0))


def seg_ids(years: np.ndarray, starts, series=None) -> np.ndarray:
    """A segment id per row: the series (if any) and the number of segment starts at or before the year."""
    k = np.searchsorted(sorted(set(starts)), years, side="right")
    return np.array([f"{s}|{i}" for s, i in zip(series if series is not None else [""] * len(years), k)])


def five_year(y, X, years, ids) -> dict:
    """Non-overlapping five-year differences within segments (each anchored at its segment's first year with data),
    Newey-West (Bartlett, 4 lags, as section 6)."""
    y, X = np.asarray(y, float), np.asarray(X, float).reshape(len(y), -1)
    years, ids = np.asarray(years, int), np.asarray(ids)
    ok = np.isfinite(y) & np.isfinite(X).all(1)
    rows = []
    for sid in sorted(set(ids[ok])):
        m = np.flatnonzero(ok & (ids == sid))
        yr = years[m]
        first = yr.min()
        at = {int(t): i for t, i in zip(yr, m)}
        for t in sorted(at):
            if (t - first) % 5 == 0 and (t - 5) in at:
                i, j = at[t], at[t - 5]
                rows.append((t, y[i] - y[j], X[i] - X[j]))
    if len(rows) < 6:
        return dict(error=f"too few five-year differences ({len(rows)})")
    rows.sort(key=lambda r: r[0])
    dy = np.array([r[1] for r in rows])
    dX = np.array([r[2] for r in rows])
    return {**infl.newey_west(dy, dX, lags=NW_LAGS), "n_differences": len(rows)}


def q_segment(years_q: np.ndarray, starts) -> tuple[int, int] | None:
    """Section 5's rule on q_US: the longest segment (cut at the documented us_q starts) by its count of q years t-1
    with an observation year t in 1948-2025; ties: the later segment."""
    if not len(years_q):
        return None
    cuts = sorted({int(years_q.min())} | {int(t) for t in starts if years_q.min() < t <= years_q.max()})
    spans = list(zip(cuts, [c - 1 for c in cuts[1:]] + [int(years_q.max())]))
    best = max(spans, key=lambda ab: (sum(1 for t in years_q if ab[0] <= t <= ab[1] and FIRST <= t + 1 <= LAST), ab[0]))
    return best


def run(half: str = "explore") -> dict:
    d, meta = fetch_series(half)
    seg = sg.load()

    def rows_of(series):
        return seg[(seg["geo"] == "US") & (seg["series"] == series)]["tau"].astype(int).tolist()
    s_cps, s_q = rows_of("us_cps"), rows_of("us_q")
    yrs = d.index.to_numpy(int)
    q = d["logq_l1"].to_numpy(float)
    ok = np.isfinite(q)
    qyears = yrs[ok] - 1                                        # the q year of each observation year's lagged q
    span = q_segment(qyears, s_q)
    inseg = ok & (yrs - 1 >= span[0]) & (yrs - 1 <= span[1]) if span else ok
    years_r = yrs[inseg]
    xs = dict(zip(years_r.tolist(), q[inseg].tolist()))
    order = sorted(years_r, key=lambda t: (xs[t], t))
    n = len(order)
    terc = {t: math.ceil(3 * (r + 1) / n) for r, t in enumerate(order)}
    k1 = 0.5 * (max(xs[t] for t in order if terc[t] == 1) + min(xs[t] for t in order if terc[t] == 2))
    k2 = 0.5 * (max(xs[t] for t in order if terc[t] == 2) + min(xs[t] for t in order if terc[t] == 3))
    P = specs.basis(q, k1, k2)
    P[~inseg] = np.nan                                          # other q segments leave U-K2 and U-Y0 (section 5)
    U = d["U"].to_numpy(float)
    out = {"knots": {"k1": k1, "k2": k2, "n": n, "q_segment": list(span) if span else None},
           "series_index_dates": meta, "no_verdict": True, "newey_west_lags": NW_LAGS}
    ids_cps = seg_ids(yrs, s_cps)
    for lab, cols in (("both", ["M2534", "F2534"]), ("men", ["M2534"]), ("women", ["F2534"])):
        y = d[cols].mean(axis=1, skipna=False).to_numpy(float)
        X = np.column_stack([P, U, dummies(yrs, s_cps)])
        r = infl.newey_west(y, X, NW_LAGS)
        V = r["se"]
        out[f"U-K2.{lab}"] = dict(g1=r["beta"][0], g3=r["beta"][2], g3_minus_g1=r["beta"][2] - r["beta"][0],
                                  se_g1=V[0], se_g3=V[2], n=r["n"])
        out[f"U-Y0.{lab}"] = dict(g1=r["beta"][0], se=V[0])
        fy = five_year(y, np.column_stack([P, U]), yrs, ids_cps)
        out[f"U-K2.{lab}.five_year"] = (fy if "error" in fy else
                                        dict(g1=fy["beta"][0], g3=fy["beta"][2], g3_minus_g1=fy["beta"][2] - fy["beta"][0],
                                             se_g1=fy["se"][0], se_g3=fy["se"][2], n=fy["n_differences"]))
        out[f"U-Y0.{lab}.five_year"] = (fy if "error" in fy else dict(g1=fy["beta"][0], se=fy["se"][0],
                                                                      n=fy["n_differences"]))
    try:
        cor = coresidence(half)
        s_cor = rows_of("us_coresid")
        ad3_first = int(cor.loc[cor["series"] == "AD-3", "year"].min())
        fwd = cor.loc[cor["series"] == "AD-1 forward", "year"]
        starts = s_cor + [ad3_first] + ([int(fwd.min())] if len(fwd) else [])
        cyr = cor["year"].to_numpy(int)
        cq = d["logq_l1"].reindex(cyr).to_numpy(float)
        cu = d["U"].reindex(cyr).to_numpy(float)
        census = (cor["series"] == "AD-1 census").to_numpy(float)[:, None]
        Xc = np.column_stack([cq, cu, dummies(cyr, starts), census])
        ids = seg_ids(cyr, starts, cor["series"].tolist())
        for lab in ("both", "men", "women"):
            yv = cor[lab].to_numpy(float)
            r = infl.newey_west(yv, Xc, NW_LAGS)
            out[f"U-C1.{lab}"] = dict(b_q=r["beta"][0], se_q=r["se"][0], b_U=r["beta"][1], se_U=r["se"][1], n=r["n"])
            fy = five_year(yv, np.column_stack([cq, cu]), cyr, ids)
            out[f"U-C1.{lab}.five_year"] = fy if "error" in fy else dict(b_q=fy["beta"][0], se_q=fy["se"][0],
                                                                          n=fy["n_differences"])
        out["U-C1.note"] = ("rows ordered by year, then series; AD-1's census points are their own segment (a dummy) "
                            "beside AD-3's values for 1970 and 1980; AD-1 forward is a new segment")
    except (ValueError, KeyError) as e:
        out["U-C1"] = dict(error=str(e))
    try:
        en = enrolment(half)
        s_en = rows_of("us_enrol")
        ey = en.reindex(yrs).to_numpy(float)
        X = np.column_stack([U, dummies(yrs, s_en + s_cps)])
        r = infl.newey_west(ey, X, NW_LAGS)
        out["U-S"] = dict(b_U=r["beta"][0], se_U=r["se"][0], n=r["n"])
        fy = five_year(ey, U[:, None], yrs, seg_ids(yrs, s_en + s_cps))
        out["U-S.five_year"] = fy if "error" in fy else dict(b_U=fy["beta"][0], se_U=fy["se"][0], n=fy["n_differences"])
        out["U-S.by_sex"] = "not run: Table A-2's both-sexes rate only (section 6, 'by sex where the series allow')"
    except (ValueError, KeyError) as e:
        out["U-S"] = dict(error=str(e))
    return out


def main() -> None:
    fetch.allowed_countries("explore")
    if os.path.exists(OUT):
        raise SystemExit(f"{OUT} exists: the US deep study runs once")
    res = run("explore")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(specs.clean_json(res), f, indent=1)
    print(f"wrote {OUT} — commit it as it came out")


if __name__ == "__main__":
    main()
