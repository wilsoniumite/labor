# common.py — shared loader and regression helper for the women_men exploration (explore half only).
#
# Everything comes through explore/data.py. Variables built from the frozen manifest's raw frames (manifest_raw) are
# marked M; those from the prefetched EXTRA series are marked X (understanding only, never an E).
# The regression helper mirrors the frozen pipeline: country and year fixed effects, C3 break dummies
# 1[geo=c, year>=tau] from every series used, 2020-2021 dropped, WCR (Webb, CR1) clustered by country.

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "explore"))
sys.path.insert(0, os.path.join(ROOT, "code"))
import data  # noqa: E402
import build  # noqa: E402
import eurostat as es  # noqa: E402
import inference as inf  # noqa: E402
import specs  # noqa: E402  (read-only use of break_dummies)

GEOS = data.GEOS
YEARS = list(range(1995, 2026))
DROP = (2020, 2021)
PRIME = build.AGES_PRIME
COUNTER = os.path.join(HERE, "spec_count.txt")


def count(n: int = 1, what: str = "") -> None:
    """Running count of estimated specifications (forking-path ledger)."""
    with open(COUNTER, "a", encoding="utf-8") as f:
        f.write(f"{n}\t{what}\n")


def total_count() -> int:
    if not os.path.exists(COUNTER):
        return 0
    return sum(int(l.split("\t")[0]) for l in open(COUNTER, encoding="utf-8") if l.strip())


_V: dict = {}


def manifest_vars() -> dict:
    """name -> (series indexed (geo, year), breaks) built from the frozen manifest raw frames only (M)."""
    if _V:
        return _V
    raw = build.cap_uk(data.manifest_raw())
    act, emp = raw["act"], raw["emp"]
    v = dict(build.panel_variables(raw, GEOS))
    for cz, suf in (("NAT", ""), ("TOTAL", "_all")):
        for s in "MF":
            for a in PRIME + build.AGES_OLD:
                v[f"A{s}{a[1:]}{suf}"] = build.cell(act, sex=s, age=a, citizen=cz)
            v[f"A{s}2534{suf}"] = build.band(act, [dict(sex=s, age=a, citizen=cz) for a in ("Y25-29", "Y30-34")])
            v[f"A{s}3544{suf}"] = build.band(act, [dict(sex=s, age=a, citizen=cz) for a in ("Y35-39", "Y40-44")])
            v[f"A{s}4554{suf}"] = build.band(act, [dict(sex=s, age=a, citizen=cz) for a in ("Y45-49", "Y50-54")])
            v[f"A{s}5564{suf}"] = build.band(act, [dict(sex=s, age=a, citizen=cz) for a in build.AGES_OLD])
            v[f"E{s}2554{suf}"] = build.band(emp, [dict(sex=s, age=a, citizen=cz) for a in PRIME])
            v[f"E{s}2024{suf}"] = build.cell(emp, sex=s, age="Y20-24", citizen=cz)
    # the long-window cycle: lfsa_urgan for every country (C7's fallback series, one source for all)
    for name, age in (("U_lfs", "Y25-74"), ("U2554_lfs", "Y25-54"), ("U1529_lfs", "Y15-29")):
        v[name] = build.cell(raw["une_lfs"], age=age)
    _V.update(v)
    return _V


def panel(names=None) -> pd.DataFrame:
    """Country-year frame of manifest variables, with name__breaks columns; 2020-2021 dropped."""
    v = manifest_vars()
    names = list(v) if names is None else names
    grid = pd.MultiIndex.from_product([GEOS, YEARS], names=["geo", "year"])
    df = pd.DataFrame(index=grid)
    for n in names:
        s, b = v[n]
        s = s[~s.index.duplicated()]
        df[n] = s.reindex(grid).to_numpy(float)
        df[n + "__breaks"] = [list(b.get(g, [])) for g in grid.get_level_values(0)]
    df = df[~np.isin(grid.get_level_values(1), DROP)]
    return df


def series_x(key: str, **sel) -> pd.Series:
    """An EXTRA series cell (X: understanding only), indexed (geo, year)."""
    d = data.extra(key)
    for k, val in sel.items():
        d = d[d[k] == val]
    s = pd.Series(d["value"].to_numpy(float), index=pd.MultiIndex.from_arrays(
        [d["geo"].astype(str), d["year"].astype(int)], names=["geo", "year"]))
    return s[~s.index.duplicated()]


def reg(df: pd.DataFrame, y, x, controls=(), years=(1997, 2025), geos=None, side=+1, B=9999, label="",
        trends=False, extra_breaks=(), use_breaks=True, fe=("geo", "year")) -> dict:
    """y, x: column names or (sign, name) lists for y. Country+year FE, C3 breaks of every series, WCR."""
    ylist = [(1, y)] if isinstance(y, str) else list(y)
    xcols = [x] if isinstance(x, str) else list(x)
    d = df.reset_index()
    d = d[(d["year"] >= years[0]) & (d["year"] <= years[1]) & ~d["year"].isin(DROP)]
    if geos is not None:
        d = d[d["geo"].isin(geos)]
    cols = [c for _, c in ylist] + xcols + list(controls)
    d = d[np.isfinite(d[cols].to_numpy(float)).all(1)].reset_index(drop=True)
    M = pd.DataFrame({"geo": d["geo"].to_numpy(), "year": d["year"].to_numpy(int)})
    yv = sum(s * d[c].to_numpy(float) for s, c in ylist)
    xv = d[xcols[0]].to_numpy(float)
    blocks = [inf.fe_matrix(M, list(fe))]
    other = xcols[1:] + list(controls)
    if other:
        blocks.append(d[other].to_numpy(float))
    if use_breaks:
        br = set()
        for c in cols + list(extra_breaks):
            bc = c + "__breaks"
            if bc in d:
                for g, bl in zip(d["geo"], d[bc]):
                    br.update((g, int(t)) for t in bl)
        blocks.append(specs.break_dummies(M, sorted(br)))
    if trends:
        t = (M["year"].to_numpy(float) - 2010) / 10
        blocks.append(np.column_stack([(M["geo"].to_numpy() == g) * t for g in sorted(set(M["geo"]))]))
    Z = np.column_stack(blocks)
    r = inf.wcr(yv, xv, Z, M["geo"].to_numpy(), side=side, B=B)
    r["mde"] = inf.mde(r["se"], r["G"])
    r["years"] = [int(M["year"].min()), int(M["year"].max())]
    r["label"] = label
    count(1, label)
    return r


def fmt(r: dict) -> str:
    return (f"{r['label']:55s} b={r['beta']:8.3f} se={r['se']:7.3f} p={r['p']:.3f} p_opp={r['p_opposite']:.3f} "
            f"n={r['n']:4d} G={r['G']:2d} G*={r['G_star']:.1f} mde={r['mde']:.2f} yrs={r['years'][0]}-{r['years'][1]}")
