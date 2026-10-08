# Adversarial vet of youth_school E1 (educ2024 on U2554 lagged one year). Explore half only; nothing logged to
# the explorer's specs_log (log=False everywhere). Run from participation/.
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.getcwd(), 'explore', 'youth_school'))
from youth import *          # noqa
import common
B = int(sys.argv[1]) if len(sys.argv) > 1 else 1999
v, cl = man()
v['U2554_l1'] = shift(*v['U2554'], 1)
v['U2554_l2'] = shift(*v['U2554'], 2)
v['U2554_f1'] = shift(*v['U2554'], -1)
v['U_l1'] = shift(*v['U'], 1)
v['UL2554_l1'] = shift(*v['UL2554'], 1)
keys = ['educ2024', 'U2554', 'U2554_l1', 'U2554_l2', 'U2554_f1', 'U_l1', 'U', 'UL2554_l1']
df, br = frame({k: v[k] for k in keys}, years=range(1997, 2026))
out = {}
def R(lbl, d, x, ctrl=(), **kw):
    r = reg(lbl, d, br, 'educ2024', x, list(ctrl), B=B, log=False, **kw)
    out[lbl] = {k: r[k] for k in ('beta', 'se', 'p', 'n', 'G', 'G_star', 'mde15', 'years')}
    return r
R('E1 replica', df, 'U2554_l1')
base = df.dropna(subset=['educ2024', 'U2554_l1'])
c6 = df.dropna(subset=['educ2024', 'U2554'])
# rows lost/gained relative to C-6
k1 = set(map(tuple, base[['geo', 'year']].values)); k0 = set(map(tuple, c6[['geo', 'year']].values))
lost = sorted(k0 - k1); gained = sorted(k1 - k0)
print('rows in C6 not in E1:', len(lost), pd.Series([g for g, _ in lost]).value_counts().to_dict(),
      'years', pd.Series([y for _, y in lost]).value_counts().sort_index().to_dict())
print('rows in E1 not in C6:', gained)
# contemporaneous U on E1's exact sample
both = df.dropna(subset=['educ2024', 'U2554_l1', 'U2554'])
R('C6 (U_t) on E1 sample', both, 'U2554')
R('E1 on common sample', both, 'U2554_l1')
R('horse race U_l1 | U_t', both, 'U2554_l1', ['U2554'])
# placebo lead and second lag
R('lead U_{t+1} on own sample', df, 'U2554_f1')
d3 = df.dropna(subset=['educ2024', 'U2554_l1', 'U2554_f1'])
R('E1 | lead', d3, 'U2554_l1', ['U2554_f1'])
R('lead | U_l1', d3, 'U2554_f1', ['U2554_l1'])
R('lag2 alone', df, 'U2554_l2')
d4 = df.dropna(subset=['educ2024', 'U2554_l1', 'U2554_l2'])
R('E1 | lag2', d4, 'U2554_l1', ['U2554_l2'])
# sample windows
R('E1 excl 2022', df[df.year != 2022], 'U2554_l1')
R('E1 excl 2008-2013', df[~df.year.between(2008, 2013)], 'U2554_l1')
R('E1 excl 2009-2014 (lag window)', df[~df.year.between(2009, 2014)], 'U2554_l1')
R('E1 2014-2025', df[df.year >= 2014], 'U2554_l1')
R('E1 no breaks', df, 'U2554_l1', use_breaks=False)
R('E1 country trends', df, 'U2554_l1', trends=True)
R('E1 with U25-74 lagged', df, 'U_l1')
# leave one out
loo = {}
for g in sorted(df.geo.unique()):
    r = reg(f'loo -{g}', df[df.geo != g], br, 'educ2024', 'U2554_l1', B=B, log=False)
    loo[g] = (r['beta'], r['p'])
out['loo'] = loo
# leave two out (worst pairs by beta)
bl = sorted(loo, key=lambda g: loo[g][0])[:4]
l2 = {}
for i, a in enumerate(bl):
    for b in bl[i + 1:]:
        r = reg(f'loo -{a}{b}', df[~df.geo.isin([a, b])], br, 'educ2024', 'U2554_l1', B=B, log=False)
        l2[a + b] = (r['beta'], r['p'])
out['loo2'] = l2
# per-country slopes (descriptive; within-country demeaned, year effects removed crudely)
M = base.copy()
for c in ['educ2024', 'U2554_l1']:
    M[c + '_d'] = M[c] - M.groupby('geo')[c].transform('mean')
    M[c + '_d'] = M[c + '_d'] - M.groupby('year')[c + '_d'].transform('mean')
sl = {g: float(np.polyfit(s['U2554_l1_d'], s['educ2024_d'], 1)[0]) for g, s in M.groupby('geo') if len(s) > 4}
out['country_slopes'] = sl
print('country slopes', {k: round(x, 2) for k, x in sorted(sl.items(), key=lambda t: t[1])})
print('years per country', base.groupby('geo').year.agg(['min', 'max', 'count']).to_dict('index'))
json.dump(out, open(os.path.join('explore', '_vet', 'e1_school_vet.json'), 'w'), indent=1, default=float)
