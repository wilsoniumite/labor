"""Population aging vs routine occupation shares (ISCO 4/7/8 at 15-64): C-5's cross-section on the explore half,
and within-country panel versions (oldratio = pop 56+ / 21-55, demo_pjan 2011+ from the manifest)."""
from common import *
import pickle, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, cl = P['cy'], P['cl']
R = raw()
occ = R['occ']
LOG = []
# realised aging 2011->2019 vs predicted
og = cy.pivot_table(index='geo', columns='year', values='oldratio')
cs = cl[['aging_pred', 'routine_change', 'stratum']].copy()
cs['aging_real'] = og[2019] - og[2011]
print(cs.round(3).sort_values('aging_pred').to_string())
print('corr pred vs real', cs[['aging_pred', 'aging_real', 'routine_change']].corr().round(2).to_string())
# C-5 style cross-section with stratum FE, WCR (cross-section: clusters = countries, one obs each)
d = cs.dropna(subset=['aging_pred', 'routine_change']).reset_index()
Z = inf.fe_matrix(d, ['stratum'])
r = inf.wcr(d.routine_change.to_numpy(), d.aging_pred.to_numpy(), Z, d.geo.to_numpy(), side=0, B=9999)
print('C-5 xsec explore (WCR, HC-ish):', {k: round(r[k], 3) for k in ['beta', 'se', 't', 'p', 'n']})
LOG.append(dict(tag='c5_xsec', beta=r['beta'], se=r['se'], p=r['p'], n=r['n']))
# panel: routine share on oldratio, FE geo+year, breaks on occ cells
oc_br = [series(occ, age='Y15-64', isco08=i)[1] for i in ['OC4', 'OC7', 'OC8', 'TOTAL']]
for y, x, ctl, kw in [('routine', 'oldratio', (), {}), ('routine', 'oldratio', ('U',), {}),
                      ('routine', 'oadr', (), {}), ('routine', 'oldratio', (), dict(trend=True))]:
    df = cy[cy.year <= 2025]
    r = fit(df, y, x, ctl, oc_br + ([{g: list(b) for g, b in cy.groupby('geo')['U__breaks'].first().items()}] if 'U' in ctl else []), side=0, **kw)
    LOG.append(dict(tag='panel', y=y, x=x, controls=list(ctl), trend=kw.get('trend', False), **{k: r[k] for k in ['beta', 'se', 'p', 'n', 'G', 'G_star', 'mde']}))
    print(f"panel {y} ~ {x} {ctl} {kw}: {fmt(r)}")
# figure
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
for g, rr in cs.iterrows():
    ax[0].scatter(rr.aging_pred, rr.routine_change, c='C0'); ax[0].annotate(g, (rr.aging_pred, rr.routine_change), fontsize=8)
    ax[1].scatter(rr.aging_real, rr.routine_change, c='C1'); ax[1].annotate(g, (rr.aging_real, rr.routine_change), fontsize=8)
ax[0].set_xlabel('predicted aging 2011-19 (C-5 measure)'); ax[0].set_ylabel('change in ISCO 4+7+8 share, 15-64, 2011-19 (pp)')
ax[1].set_xlabel('realised change in pop 56+/21-55, 2011-19')
for a in ax: a.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig3_aging_routine.png'), dpi=110)
json.dump(LOG, open(os.path.join(OUT, 'speclog_s06.json'), 'w'), indent=1, default=float)
print('specs', len(LOG))
