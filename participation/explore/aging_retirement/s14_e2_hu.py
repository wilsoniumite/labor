"""E2 with a realised-aging measure that survives an open-ended age group below 100 (HU 2011 reports 85+ as Y_OPEN,
single ages 85-99 missing, so the frozen C-5 aging_pred and the strict oldratio are NaN for HU). Old = every
non-missing cell aged 56+ incl. Y_OPEN; working age = single ages 21-55, all required."""
from common import *
import pickle, json
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cl = P['cl']
pop = es.clean(raw()['pop'])
pop['a'] = pop.age.map(lambda a: 999 if a == 'Y_OPEN' else int(a[1:]))
def ratio(g, y):
    d = pop[(pop.geo == g) & (pop.year == y)]
    w = d[(d.a >= 21) & (d.a <= 55)]
    if len(w) != 35 or w.value.isna().any(): return np.nan
    o = d[(d.a >= 56) & (d.a <= 84)]
    if len(o) != 29 or o.value.isna().any(): return np.nan
    return d[d.a >= 56].value.sum() / w.value.sum()
X = cl[['stratum', 'routine_change']].copy()
X['aging_real'] = [ratio(g, 2019) - ratio(g, 2011) for g in X.index]
print(X.round(3).to_string())
d = X.dropna().reset_index()
r = inf.wcr(d.routine_change.to_numpy(), d.aging_real.to_numpy(), inf.fe_matrix(d, ['stratum']), d.geo.to_numpy(), side=+1, B=9999)
r['mde15'] = inf.mde(r['se'], 15)
print({k: round(r[k], 4) for k in ['beta', 'se', 't', 'p', 'p_opposite', 'n', 'G', 'G_star', 'mde15']})
loo = {}
for g in d.geo:
    dd = d[d.geo != g]
    rr = inf.wcr(dd.routine_change.to_numpy(), dd.aging_real.to_numpy(), inf.fe_matrix(dd, ['stratum']), dd.geo.to_numpy(), side=+1, B=1999)
    loo[g] = (round(rr['beta'], 2), round(rr['p'], 3))
print('LOO', loo)
c = json.load(open(os.path.join(OUT, 'candidates_explore.json')))
c['E2_real_aging_routine_withHU'] = dict(r, loo=loo, rows=d.round(4).values.tolist())
json.dump(c, open(os.path.join(OUT, 'candidates_explore.json'), 'w'), indent=1, default=float)
