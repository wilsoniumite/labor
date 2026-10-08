"""The ownership interaction: robustness for the old-minus-prime gap, and country-by-country slopes of the gap on
log(HPI/CPI) against outright ownership (figure)."""
from common import *
import pickle, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, brk = P['cy'].copy(), P['brk']
cy['A2554'] = (cy.AW2554 + cy.AM2554) / 2
cy['G_old'] = cy.A5564 - cy.A2554
own = cy.groupby('geo').owner_outright_5564.first()
cy['own_std'] = cy.geo.map((own - own.mean()) / own.std(ddof=0))
cy['hpi_own'] = cy.logq_hpi_l1 * cy.own_std
cy['cee'] = (cy.stratum == 'CEE').astype(int)
cy['yc'] = cy.year.astype(str) + '_' + cy.cee.astype(str)
def bl(n):
    return {g: list(b) for g, b in cy.groupby('geo')[n + '__breaks'].first().items()}
BR = [bl('A5564'), bl('AW2554'), bl('AM2554'), bl('logq_hpi_l1'), bl('U')]
LOG = []
for tag, kw in [('trend', dict(trend=True)), ('ceeXyear', dict(fe=('geo', 'yc'))), ('noU', dict(controls=('logq_hpi_l1',)))]:
    ctl = kw.pop('controls', ('U', 'logq_hpi_l1'))
    r = fit(cy, 'G_old', 'hpi_own', ctl, BR, side=0, **kw)
    LOG.append(dict(tag=tag, **{k: r[k] for k in ['beta', 'se', 'p', 'n', 'G', 'G_star', 'mde']}))
    print(tag, fmt(r))
for g in sorted(cy.geo.unique()):
    r = fit(cy[cy.geo != g], 'G_old', 'hpi_own', ('U', 'logq_hpi_l1'), BR, side=0, B=1999)
    print('  LOO drop', g, f"b={r['beta']:.2f} t={r['t']:.2f} p={r['p']:.3f}")
# country slopes (OLS within country, U control, no breaks): descriptive
rows = []
for g, d in cy.dropna(subset=['G_old', 'logq_hpi_l1', 'U']).groupby('geo'):
    if len(d) < 8: continue
    X = np.column_stack([np.ones(len(d)), d.logq_hpi_l1, d.U, d.year - 2015])
    b = np.linalg.lstsq(X, d.G_old, rcond=None)[0]
    rows.append((g, own[g], b[1], d.logq_hpi_l1.std(), len(d)))
S = pd.DataFrame(rows, columns=['geo', 'own', 'slope', 'sd_hpi', 'n'])
print(S.round(2).to_string())
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(S.own, S.slope, s=20 + 300 * S.sd_hpi)
for _, r in S.iterrows(): ax.annotate(r.geo, (r.own, r.slope), fontsize=8)
ax.axhline(0, c='k', lw=.5); ax.grid(alpha=.3)
ax.set_xlabel('outright owners among 55-64, % (2015-17)')
ax.set_ylabel('slope of A(55-64) - A(25-54) on log(HPI/CPI)_{t-1}\n(within country, U and linear trend held)')
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig4_own_slopes.png'), dpi=110)
json.dump(LOG, open(os.path.join(OUT, 'speclog_s11.json'), 'w'), indent=1, default=float)
