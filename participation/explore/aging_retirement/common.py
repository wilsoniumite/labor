"""Shared loaders for the aging/retirement exploration (explore half only, all data through explore/data.py)."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'explore')); sys.path.insert(0, os.path.join(ROOT, 'code'))
import numpy as np
import pandas as pd
import data
import eurostat as es
import inference as inf

OUT = os.path.join(ROOT, 'explore', 'aging_retirement')
GEOS = data.GEOS
_cache = {}


def raw():
    if 'raw' not in _cache:
        _cache['raw'] = data.manifest_raw()
    return _cache['raw']


def extra(k):
    if k not in _cache:
        _cache[k] = data.extra(k)
    return _cache[k]


def series(df, **sel):
    """clean values indexed (geo, year) and break years per geo."""
    d = df
    for k, v in sel.items():
        d = d[d[k] == v]
    br = es.break_years(d)
    c = es.clean(d)
    s = pd.Series(c['value'].to_numpy(float), index=pd.MultiIndex.from_arrays([c.geo.astype(str), c.year.astype(int)],
                                                                            names=['geo', 'year']))
    return s[~s.index.duplicated()], br


def act(age, sex, cz='NAT', src='manifest'):
    df = raw()['act'] if src == 'manifest' else extra('argan')
    return series(df, age=age, sex=sex, citizen=cz)


def breaks_matrix(df, brs):
    """C3 dummies 1[geo=c, year>=tau] for every (c, tau) in the union of brs (dicts geo->years)."""
    cols = {}
    for b in brs:
        for g, ys in b.items():
            for y in ys:
                cols[(g, int(y))] = ((df['geo'] == g) & (df['year'] >= int(y))).astype(float).to_numpy()
    if not cols:
        return np.zeros((len(df), 0))
    M = np.column_stack(list(cols.values()))
    keep = M.std(0) > 0
    return M[:, keep]


def fit(df, y, x, controls=(), brs=(), fe=('geo', 'year'), side=-1, B=9999, trend=False):
    d = df.dropna(subset=[y, x] + list(controls)).reset_index(drop=True)
    parts = [inf.fe_matrix(d, list(fe))]
    if controls:
        parts.append(d[list(controls)].to_numpy(float))
    if brs:
        parts.append(breaks_matrix(d, brs))
    if trend:
        for g in sorted(d.geo.unique()):
            parts.append(((d.geo == g) * (d.year - 2010)).to_numpy(float)[:, None])
    Z = np.column_stack(parts)
    r = inf.wcr(d[y].to_numpy(float), d[x].to_numpy(float), Z, d['geo'].to_numpy(), side=side, B=B)
    r['mde'] = inf.mde(r['se'], r['G'])
    r['years'] = f"{d.year.min()}-{d.year.max()}"
    return r


def fmt(r):
    return (f"b={r['beta']:.3f} se={r['se']:.3f} t={r['t']:.2f} p={r['p']:.3f} p_opp={r['p_opposite']:.3f} "
            f"n={r['n']} G={r['G']} G*={r['G_star']:.1f} MDE={r['mde']:.3f} yrs={r['years']}")
