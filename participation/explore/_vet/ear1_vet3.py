"""E-AR1 vet, part 3: LU and the window; the exit-margin (55-64 minus 45-54) version. Explore half, manifest act only."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'explore')); sys.path.insert(0, os.path.join(ROOT, 'code'))
import numpy as np, pandas as pd
import data, eurostat as es, inference as inf
R = data.manifest_raw(); c = es.clean(R['act']); c['year'] = c.year.astype(int)
STR = {g: s for s, gs in es.STRATA.items() for g in gs}
def band(ages, sexes=('M', 'F')):
    d = c[(c.citizen == 'NAT') & c.age.isin(ages) & c.sex.isin(sexes)]
    w = d.pivot_table(index=['geo', 'year'], columns=['sex', 'age'], values='value', aggfunc='first')
    m = w.mean(axis=1); m[w.notna().sum(axis=1) < len(ages) * len(sexes)] = np.nan
    return m.unstack('year')
A = band(['Y55-59', 'Y60-64']); C = band(['Y45-49', 'Y50-54'])
print('LU cells 55-64 NAT 2009:'); print(R['act'][(R['act'].geo=='LU')&(R['act'].year.astype(int)==2009)&R['act'].age.isin(['Y55-59','Y60-64'])&(R['act'].citizen=='NAT')][['sex','age','value','flag']])
def xs(name, y, xv, drop=(), side=-1):
    d = pd.DataFrame({'y': y, 'x': xv}).dropna(); d = d[~d.index.isin(drop)]
    d = d.reset_index().rename(columns={'index': 'geo'}); d['stratum'] = d.geo.map(STR)
    r = inf.wcr(d.y.to_numpy(), d.x.to_numpy(), inf.fe_matrix(d, ['stratum']), d.geo.to_numpy(), side=side, B=9999)
    print(f"{name:50s} b={r['beta']:+.3f} se={r['se']:.3f} p={r['p']:.4f} G={r['G']} mde15={inf.mde(r['se'],15):.3f}")
for y0 in [2011, 2012]:
    xs(f'{y0}-2019 with LU', A[2019] - A[y0], A[y0])
    xs(f'{y0}-2019 without LU', A[2019] - A[y0], A[y0], drop=['LU'])
xs('2009-2019 with LU at its 2011 level (imputed, check)', (A[2019] - A[2009]).fillna(A[2019]-A[2011]), A[2009].fillna(A[2011]))
G = A - C
xs('exit margin: d(A5564-A4554) 09-19 on gap09', G[2019] - G[2009], G[2009])
xs('exit margin 09-19 without LU (n/a anyway)', G[2019] - G[2009], G[2009], drop=['LU'])
print(G[[2009, 2019]].round(1).to_string())
