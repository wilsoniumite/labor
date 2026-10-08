"""Adversarial vet of E-AR2 (old-minus-prime activity gap on log(HPI/CPI)_{t-1} x outright ownership 55-64).
Explore half only; data through explore/data.py (via the aging_retirement common loaders, read-only)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'aging_retirement'))
from common import *   # noqa
B = int(os.environ.get('VB', '9999'))
cy, cl = data.panel(); cy = cy.reset_index()
cy = cy.merge(cl[['owner_outright_5564', 'stratum']].reset_index(), on='geo', how='left')
cy['A2554'] = (cy.AW2554 + cy.AM2554) / 2
cy['G_old'] = cy.A5564 - cy.A2554
cy['G_old_all'] = cy.A5564_all - (cy.AW2554_all + cy.AM2554_all) / 2
own = cl.owner_outright_5564
def std(s): return (s - s.mean()) / s.std(ddof=0)
cy['own_std'] = cy.geo.map(std(own))
cy['hpi_own'] = cy.logq_hpi_l1 * cy.own_std
cy['rent_own'] = cy.logq_l1 * cy.own_std
cy['cee'] = (cy.stratum == 'CEE').astype(float)
cy['hpi_cee'] = cy.logq_hpi_l1 * cy.cee
cy = cy.sort_values(['geo', 'year'])
# lead: logq_hpi at t+1 = logq_hpi_l1 at t+2 (consecutive years only)
nxt = cy.groupby('geo').logq_hpi_l1.shift(-2)
ok = cy.groupby('geo').year.shift(-2) == cy.year + 2
cy['hpi_f1'] = nxt.where(ok)
cy['hpi_f1_own'] = cy.hpi_f1 * cy.own_std
def bl(n): return {g: list(b) for g, b in cy.groupby('geo')[n + '__breaks'].first().items()}
BR = [bl('A5564'), bl('AW2554'), bl('AM2554'), bl('logq_hpi_l1'), bl('U')]
BRall = [bl('A5564_all'), bl('AW2554_all'), bl('AM2554_all'), bl('logq_hpi_l1'), bl('U')]
BRr = [bl('A5564'), bl('AW2554'), bl('AM2554'), bl('logq_l1'), bl('U')]
LOG = {}
N = [0]
def run(tag, d, y, x, ctl, brs, side=+1, **kw):
    r = fit(d, y, x, ctl, brs, side=side, B=B, **kw)
    N[0] += 1
    LOG[tag] = {k: (float(r[k]) if not isinstance(r[k], str) else r[k]) for k in ['beta', 'se', 't', 'p', 'p_opposite', 'n', 'G', 'G_star', 'mde']}
    print(f"{tag:28s} {fmt(r)}")
    return r
C = ('U', 'logq_hpi_l1')
run('main', cy, 'G_old', 'hpi_own', C, BR)
run('A5564_only', cy, 'A5564', 'hpi_own', C, BR)
run('A2554_only(pred -)', cy, 'A2554', 'hpi_own', C, BR, side=-1)
run('all_residents', cy, 'G_old_all', 'hpi_own', C, BRall)
run('rent_q_x_own', cy, 'G_old', 'rent_own', ('U', 'logq_l1'), BRr)
run('excl_2008_2013', cy[~cy.year.between(2008, 2013)], 'G_old', 'hpi_own', C, BR)
run('lead_added', cy, 'G_old', 'hpi_own', C + ('hpi_f1', 'hpi_f1_own'), BR)
run('lead_alone_placebo', cy, 'G_old', 'hpi_f1_own', ('U', 'hpi_f1'), BR)
run('mod=CEE_dummy', cy, 'G_old', 'hpi_cee', C, BR)
nc = cy[cy.cee == 0].copy(); o2 = std(own[own.index.isin(nc.geo.unique())])
nc['hpi_own'] = nc.logq_hpi_l1 * nc.geo.map(o2)
run('nonCEE_only(9)', nc, 'G_old', 'hpi_own', C, BR)
ce = cy[cy.cee == 1].copy(); o3 = std(own[own.index.isin(ce.geo.unique())])
ce['hpi_own'] = ce.logq_hpi_l1 * ce.geo.map(o3)
run('CEE_only(7)', ce, 'G_old', 'hpi_own', C, BR)
run('trend', cy, 'G_old', 'hpi_own', C, BR, trend=True)
run('2009plus', cy[cy.year >= 2009], 'G_old', 'hpi_own', C, BR)
# LOO, one-sided
loo = {}
for g in sorted(cy.geo.unique()):
    d = cy[cy.geo != g].copy(); o = std(own.drop(g)); d['hpi_own'] = d.logq_hpi_l1 * d.geo.map(o)
    r = fit(d, 'G_old', 'hpi_own', C, BR, side=+1, B=B)
    loo[g] = (round(r['beta'], 2), round(r['t'], 2), round(r['p'], 3), round(r['G_star'], 1))
    print('LOO', g, loo[g])
LOG['loo_restd'] = loo
# drop SE and CH (the two low-ownership countries)
d = cy[~cy.geo.isin(['SE', 'CH'])].copy(); o = std(own.drop(['SE', 'CH'])); d['hpi_own'] = d.logq_hpi_l1 * d.geo.map(o)
run('drop_SE_CH', d, 'G_old', 'hpi_own', C, BR)
# randomisation inference: permute ownership across countries (t statistic, CR1)
d0 = cy.dropna(subset=['G_old', 'hpi_own', 'U', 'logq_hpi_l1']).reset_index(drop=True)
Z0 = np.column_stack([inf.fe_matrix(d0, ['geo', 'year']), d0[['U', 'logq_hpi_l1']].to_numpy(float), breaks_matrix(d0, BR)])
geos = np.array(sorted(d0.geo.unique())); os_ = std(own.loc[geos]).to_numpy()
def tstat(xv):
    r = inf.wcr(d0.G_old.to_numpy(float), xv, Z0, d0.geo.to_numpy(), side=1, B=9)
    return r['t'], r['beta']
t0, b0 = tstat(d0.logq_hpi_l1.to_numpy() * d0.geo.map(dict(zip(geos, os_))).to_numpy())
rng = np.random.default_rng(7); ts = []; bs = []
for _ in range(1999):
    p = rng.permutation(os_)
    t, b = tstat(d0.logq_hpi_l1.to_numpy() * d0.geo.map(dict(zip(geos, p))).to_numpy()); ts.append(t); bs.append(b)
ts = np.array(ts); bs = np.array(bs)
LOG['ri_perm_own'] = dict(t0=t0, b0=b0, p_t=float((1 + (ts >= t0).sum()) / 2000), p_b=float((1 + (bs >= b0).sum()) / 2000))
print('RI permute ownership:', LOG['ri_perm_own'])
# country slopes descriptives
rows = []
for g, dd in d0.groupby('geo'):
    X = np.column_stack([np.ones(len(dd)), dd.logq_hpi_l1, dd.U])
    b = np.linalg.lstsq(X, dd.G_old, rcond=None)[0]
    rows.append((g, round(own[g], 1), round(b[1], 1), round(dd.logq_hpi_l1.max() - dd.logq_hpi_l1.min(), 2), round(dd.G_old.iloc[-1] - dd.G_old.iloc[0], 1), len(dd)))
print(pd.DataFrame(rows, columns=['geo', 'own', 'slope_noTrend', 'range_lq', 'dGap', 'n']).to_string())
LOG['n_specs_vet'] = N[0]
json.dump(LOG, open(os.path.join(HERE, 'ar2_vet.json'), 'w'), indent=1, default=float)
print('vet specs', N[0])
