"""Aging and prices / structure: (i) does the old-age ratio go with rising q or house prices within country (older
owners are net long and hold more space per head)? (ii) routine change 2011-19 on realised aging (pop 56+/21-55,
2011->2019) with stratum effects; (iii) where does q's within-country variation come from (G* diagnosis)."""
from common import *
import pickle, json
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, cl = P['cy'].copy(), P['cl']
LOG = []
def brs_of(*names):
    out = []
    for n in names:
        if n + '__breaks' in cy:
            out.append({g: list(b) for g, b in cy.groupby('geo')[n + '__breaks'].first().items()})
    return out
for y in ['logq', 'logq_hpi_l1', 'coresid2534']:
    r = fit(cy, y, 'oldratio', (), brs_of(y), side=0)
    LOG.append(dict(tag='aging_prices', y=y, x='oldratio', **{k: r[k] for k in ['beta', 'se', 'p', 'n', 'G', 'G_star', 'mde']}))
    print(f"{y:12s} ~ oldratio: {fmt(r)}")
og = cy.pivot_table(index='geo', columns='year', values='oldratio')
d = cl[['routine_change', 'stratum', 'aging_pred']].copy()
d['aging_real'] = og[2019] - og[2011]
d = d.dropna(subset=['routine_change', 'aging_real']).reset_index()
r = inf.wcr(d.routine_change.to_numpy(), d.aging_real.to_numpy(), inf.fe_matrix(d, ['stratum']), d.geo.to_numpy(), side=0)
LOG.append(dict(tag='routine_real_aging', **{k: r[k] for k in ['beta', 'se', 'p', 'n', 'G']}))
print('routine_change ~ aging_real + stratum FE:', {k: round(r[k], 3) for k in ['beta', 'se', 't', 'p', 'n']})
# q variation by country after FE
d2 = cy.dropna(subset=['logq_l1', 'A5564', 'U']).copy()
Z = inf.fe_matrix(d2, ['geo', 'year'])
Q = np.column_stack([np.ones(len(d2)), Z])
xt = d2.logq_l1 - Q @ np.linalg.lstsq(Q, d2.logq_l1, rcond=None)[0]
print('share of residual q variance by country:', (xt ** 2).groupby(d2.geo).sum().div((xt ** 2).sum()).round(3).sort_values(ascending=False).to_dict())
json.dump(LOG, open(os.path.join(OUT, 'speclog_s09.json'), 'w'), indent=1, default=float)
print('specs', len(LOG))
