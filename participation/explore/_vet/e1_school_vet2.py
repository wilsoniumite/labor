# E1 as stated: U2554 lagged on the full annual grid (2021's U enters the 2022 row), built from manifest raw frames.
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.getcwd(), 'explore', 'youth_school'))
from youth import *          # noqa
import build, data
B = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
r = raw()
U = build._by_country(cell(r['une'], age='Y25-54'), cell(r['une_lfs'], age='Y25-54'), data.GEOS)
U74 = build._by_country(cell(r['une'], age='Y25-74'), cell(r['une_lfs'], age='Y25-74'), data.GEOS)
src = {g: ('une' if g in set(cell(r['une'], age='Y25-54')[0].dropna().index.get_level_values(0)) else 'une_lfs') for g in data.GEOS}
print('source per country', src)
ed = cell(r['educ'])
v = {'educ2024': ed, 'U2554': U, 'U2554_l1': build._shift(*U, 1), 'U_l1': build._shift(*U74, 1)}
print('U2554 2021 present:', U[0].xs(2021, level=1).dropna().shape[0], 'countries; breaks U2554:', U[1], '\nbreaks educ:', ed[1])
df, br = frame(v, years=range(1997, 2026))
res = {}
def R(l, d, x, **kw):
    o = reg(l, d, br, 'educ2024', x, B=B, log=False, **kw); res[l] = {k: o[k] for k in ('beta','se','p','n','G','G_star','mde15','years')}; return o
R('E1 as stated (2022 uses U2021)', df, 'U2554_l1')
R('E1 as stated, excl 2022', df[df.year != 2022], 'U2554_l1')
R('E1 as stated, country trends', df, 'U2554_l1', trends=True)
R('E1 as stated, excl 2008-2013', df[~df.year.between(2008, 2013)], 'U2554_l1')
R('C6 replica', df, 'U2554')
d = df.dropna(subset=['educ2024', 'U2554_l1', 'U2554'])
R('C6 on E1-as-stated sample', d, 'U2554')
# leave-one-out of the stated version
loo = {}
for g in sorted(df.geo.unique()):
    o = reg(f'loo -{g}', df[df.geo != g], br, 'educ2024', 'U2554_l1', B=1999, log=False); loo[g] = (o['beta'], o['p'])
res['loo'] = loo
print('loo beta range', min(b for b, _ in loo.values()), max(b for b, _ in loo.values()), 'max p', max(p for _, p in loo.values()))
# 2022 residual check: change 2019->2022 in educ vs U2021-U2018
w = df.set_index(['geo', 'year'])
json.dump(res, open(os.path.join('explore', '_vet', 'e1_school_vet2.json'), 'w'), indent=1, default=float)
