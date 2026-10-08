"""Robustness of the positive (old participation x house prices x outright ownership) interaction: country trends,
stratum-by-year effects (CEE x year), dropping each country, and the reading by stratum."""
from common import *
import pickle, json
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, brk = P['cy'], P['brk']
own = cy.groupby('geo').owner_outright_5564.first()
cy['own_std'] = cy.geo.map((own - own.mean()) / own.std(ddof=0))
cy['cee'] = (cy.stratum == 'CEE').astype(int)
LOG = []
def brs_of(*names):
    out = []
    for n in names:
        if n in brk: out.append(brk[n])
        elif n + '__breaks' in cy:
            out.append({g: list(b) for g, b in cy.groupby('geo')[n + '__breaks'].first().items()})
    return out
def run(df, y, x, controls=('U',), side=0, tag='', fe=('geo', 'year'), **kw):
    r = fit(df, y, x, controls, brs_of(y, x, *[c for c in controls if not c.startswith('d_')]), side=side, fe=fe, **kw)
    LOG.append(dict(tag=tag, y=y, x=x, controls=list(controls), side=side, **{k: r[k] for k in ['beta', 'se', 'p', 'p_opposite', 'n', 'G', 'G_star', 'mde']}, years=r['years'], trend=kw.get('trend', False)))
    print(f"{tag:10s} {y:8s} ~ {x:16s}{' trend' if kw.get('trend') else ''}: {fmt(r)}")
    return r
x = 'logq_hpi_l1'
cy[x + '_own'] = cy[x] * cy['own_std']
for y in ['A5564', 'AW6064']:
    run(cy, y, x + '_own', ('U', x), tag='trend', trend=True)
# CEE x year effects
cy['yc'] = cy.year.astype(str) + '_' + cy.cee.astype(str)
for y in ['A5564', 'AW6064']:
    run(cy, y, x + '_own', ('U', x), tag='ceeXyear', fe=('geo', 'yc'))
# leave one out for AW6064
for g in sorted(cy.geo.unique()):
    r = fit(cy[cy.geo != g], 'AW6064', x + '_own', ('U', x), brs_of('AW6064', x, 'U'), side=0, B=1999)
    print('  LOO drop', g, f"b={r['beta']:.2f} t={r['t']:.2f}")
json.dump(LOG, open(os.path.join(OUT, 'speclog_s05.json'), 'w'), indent=1)
print('specs', len(LOG), '+ 16 LOO (diagnostic)')
