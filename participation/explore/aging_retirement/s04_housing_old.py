"""Older participation on q and house prices, within country (FE geo+year, U, C3 breaks). Two-sided look first."""
from common import *
import pickle, json
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, brk = P['cy'], P['brk']
own = cy.groupby('geo').owner_outright_5564.first()
cy['own_std'] = cy.geo.map((own - own.mean()) / own.std(ddof=0))
LOG = []
def brs_of(*names):
    out = []
    for n in names:
        if n in brk: out.append(brk[n])
        elif n + '__breaks' in cy:
            out.append({g: list(b) for g, b in cy.groupby('geo')[n + '__breaks'].first().items()})
    return out
def run(y, x, controls=('U',), extra_br=(), side=0, tag='', **kw):
    r = fit(cy, y, x, controls, brs_of(y, x, *controls, *extra_br), side=side, **kw)
    LOG.append(dict(tag=tag, y=y, x=x, controls=list(controls), side=side, **{k: r[k] for k in ['beta', 'se', 'p', 'p_opposite', 'n', 'G', 'G_star', 'mde']}, years=r['years'], trend=kw.get('trend', False)))
    print(f"{tag:10s} {y:8s} ~ {x:14s} [{','.join(controls)}]{' trend' if kw.get('trend') else ''}: {fmt(r)}")
    return r
# build band outcomes in parts
for y in ['A5564', 'AW6064', 'AM6064', 'AW5559', 'AM5559']:
    for x in ['logq_l1', 'logq_hpi_l1']:
        run(y, x, tag='main')
# interaction with outright ownership (std across explore countries)
for x in ['logq_l1', 'logq_hpi_l1']:
    cy[x + '_own'] = cy[x] * cy['own_std']
    for y in ['A5564', 'AW6064', 'AM6064']:
        run(y, x + '_own', controls=('U', x), tag='x_own')
json.dump(LOG, open(os.path.join(OUT, 'speclog_s04.json'), 'w'), indent=1)
print('specs', len(LOG))
