# common.py — helpers for the youth/schooling exploration (explore half only, via explore/data.py).
#
# Series are (values indexed (geo, year), {geo: [break years]}) as in code/build.py; reg() runs a two-way FE
# regression with C3 break dummies and the restricted WCR (16 clusters at most), and appends every estimate to
# specs_log.jsonl so the count of specifications estimated is honest.

from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "explore"))
sys.path.insert(0, os.path.join(ROOT, "code"))
import build  # noqa: E402
import data  # noqa: E402
import inference as inf  # noqa: E402

LOG = os.path.join(HERE, "specs_log.jsonl")
EXCL = (2020, 2021)
_cache: dict = {}


def raw():
    if "raw" not in _cache:
        _cache["raw"] = data.manifest_raw()
    return _cache["raw"]


def extra(k):
    if k not in _cache:
        _cache[k] = data.extra(k)
    return _cache[k]


def panel():
    if "panel" not in _cache:
        _cache["panel"] = data.panel()
    return _cache["panel"]


cell, band, union, shift = build.cell, build.band, build._union, build._shift


def by_country(primary, fallback):
    return build._by_country(primary, fallback, data.GEOS)


def combine(fn, *series):
    """Elementwise fn over aligned series; breaks the union."""
    df = pd.concat([s for s, _ in series], axis=1)
    return fn(*[df.iloc[:, i] for i in range(df.shape[1])]), union(*[b for _, b in series])


class Breaks(dict):
    """Break years per column: {column: {geo: [years]}}. Derived columns get an alias with alias(new, *sources)."""
    def alias(self, new, *src):
        self[new] = union(*[self.get(c, {}) for c in src])


def frame(series: dict, years=None, geos=None) -> tuple[pd.DataFrame, Breaks]:
    """A (geo, year) frame of the named series and, per column, its break years (C3 acts on the series in each
    regression only: reg() unions the breaks of its outcome, regressor and controls)."""
    df = pd.concat({k: s for k, (s, _) in series.items()}, axis=1)
    df.index.names = ["geo", "year"]
    df = df.reset_index()
    if years is not None:
        df = df[df["year"].isin(list(years))]
    df = df[~df["year"].isin(EXCL)]
    if geos is not None:
        df = df[df["geo"].isin(geos)]
    return df.reset_index(drop=True), Breaks({k: b for k, (_, b) in series.items()})


def break_dummies(M, breaks: dict) -> np.ndarray:
    cols, seen = [], set()
    geo, year = M["geo"].to_numpy(), M["year"].to_numpy()
    for g, ys in breaks.items():
        m = geo == g
        if not m.any():
            continue
        for t in ys:
            col = (m & (year >= t)).astype(float)
            if col[m].min() == col[m].max():
                continue
            k = col.tobytes()
            if k not in seen:
                seen.add(k)
                cols.append(col)
    return np.column_stack(cols) if cols else np.zeros((len(M), 0))


def reg(label, df, breaks, y, x, controls=(), side=1, fe=("geo", "year"), trends=False, B=9999, use_breaks=True,
        log=True, extra_Z=None):
    """y on x with FE, controls and C3 breaks; restricted WCR one-sided in `side`. Logged as one specification."""
    cols = [y, x] + list(controls)
    M = df.dropna(subset=cols).reset_index(drop=True)
    if isinstance(breaks, Breaks):
        missing = [c for c in cols if c not in breaks]
        if missing:
            raise KeyError(f"no break record for {missing}: alias derived columns")
        breaks = union(*[breaks[c] for c in cols])
    blocks = [inf.fe_matrix(M, list(fe)) if fe else np.zeros((len(M), 0)),
              M[list(controls)].to_numpy(float).reshape(len(M), -1)]
    if use_breaks:
        blocks.append(break_dummies(M, breaks))
    if trends:
        t = (M["year"].to_numpy(float) - 2010) / 10
        blocks.append(np.column_stack([(M["geo"].to_numpy() == g) * t for g in sorted(set(M["geo"]))]))
    if extra_Z is not None:
        blocks.append(extra_Z(M))
    Z = np.column_stack(blocks)
    r = inf.wcr(M[y].to_numpy(float), M[x].to_numpy(float), Z, M["geo"].to_numpy(), side=side, B=B)
    out = dict(label=label, y=y, x=x, controls=list(controls), fe=list(fe) if fe else [], trends=trends, side=side,
               beta=r["beta"], se=r["se"], p=r["p"], p_opposite=r["p_opposite"], n=r["n"], G=r["G"],
               G_star=r.get("G_star"), mde15=inf.mde(r["se"], 15),
               years=f"{int(M['year'].min())}-{int(M['year'].max())}", geos=sorted(set(M["geo"])))
    if log:
        with open(LOG, "a") as f:
            f.write(json.dumps(out) + "\n")
    print(f"[{label}] b={out['beta']:.4g} se={out['se']:.3g} p({'+' if side > 0 else '-'})={out['p']:.4f} "
          f"n={out['n']} G={out['G']} G*={out['G_star']:.1f} yrs={out['years']} mde15={out['mde15']:.3g}")
    return out


def wide(s: pd.Series) -> pd.DataFrame:
    return s.unstack("year")
