"""E-AR1 vet, part 2: where in time the convergence sits, and cohort replacement vs within-cohort exit.
Explore half, manifest act only. Run from participation/."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'explore')); sys.path.insert(0, os.path.join(ROOT, 'code'))
import numpy as np, pandas as pd
import data, eurostat as es, inference as inf
R = data.manifest_raw(); c = es.clean(R['act']); c['year'] = c.year.astype(int)
STR = {g: s for s, gs in es.STRATA.items() for g in gs}
def band(ages, cz='NAT', sexes=('M', 'F')):
    d = c[(c.citizen == cz) & c.age.isin(ages) & c.sex.isin(sexes)]
    w = d.pivot_table(index=['geo', 'year'], columns=['sex', 'age'], values='value', aggfunc='first')
    m = w.mean(axis=1); m[w.notna().sum(axis=1) < len(ages) * len(sexes)] = np.nan
    return m.unstack('year')
A = band(['Y55-59', 'Y60-64']); C = band(['Y45-49', 'Y50-54'])
print('annual 55-64 levels, explore half')
print(A.loc[:, 2008:2019].round(1).to_string())
x = A[2009]
print('\ncorr of each one-year change with the 2009 level (n):')
for y in range(2010, 2020):
    d = (A[y] - A[y - 1]); ok = d.notna() & x.notna()
    print(y, round(np.corrcoef(d[ok], x[ok])[0, 1], 2), int(ok.sum()), 'mean change %.2f' % d[ok].mean())
nspec = 0
def xs(name, y, xv, side=-1):
    global nspec; nspec += 1
    d = pd.DataFrame({'y': y, 'x': xv}).dropna().reset_index().rename(columns={'index': 'geo'})
    d['stratum'] = d.geo.map(STR)
    r = inf.wcr(d.y.to_numpy(), d.x.to_numpy(), inf.fe_matrix(d, ['stratum']), d.geo.to_numpy(), side=side, B=9999)
    print(f"{name:55s} b={r['beta']:+.3f} se={r['se']:.3f} p={r['p']:.4f} G={r['G']}")
print('\ncohort decomposition: A5564(2019) - A5564(2009) = [A5564(19) - A4554(09)] + [A4554(09) - A5564(09)]')
xs('within-cohort exit A5564_19 - A4554_09 on A5564_09', A[2019] - C[2009], x)
xs('cohort replacement A4554_09 - A5564_09 on A5564_09', C[2009] - x, x)
xs('within-cohort exit on A4554_09 (own cohort level)', A[2019] - C[2009], C[2009])
xs('E-AR1 with A4554_09 control? (dA on A09, partial C09) -> see below', A[2019] - x, x)
d = pd.DataFrame({'y': A[2019] - x, 'x': x, 'c': C[2009]}).dropna().reset_index().rename(columns={'index': 'geo'})
d['stratum'] = d.geo.map(STR)
Z = np.column_stack([inf.fe_matrix(d, ['stratum']), d.c.to_numpy()])
r = inf.wcr(d.y.to_numpy(), d.x.to_numpy(), Z, d.geo.to_numpy(), side=-1, B=9999); nspec += 1
print(f"{'dA5564 on A5564_09, controlling A4554_09':55s} b={r['beta']:+.3f} se={r['se']:.3f} p={r['p']:.4f} G={r['G']}")
print('specs in vet2:', nspec)
