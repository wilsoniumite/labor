"""Old minus prime-age participation (differences out country-year shocks common to ages: cycle, convergence, wage
pass-through) on house prices and rents. Net-long older owners vs hedged/net-short prime-age: predicted < 0."""
from common import *
import pickle, json
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, brk = P['cy'].copy(), P['brk']
cy['A2554'] = (cy.AW2554 + cy.AM2554) / 2
cy['G_old'] = cy.A5564 - cy.A2554
cy['G_oldW'] = cy.AW6064 - cy.AW2554
cy['G_oldM'] = cy.AM6064 - cy.AM2554
own = cy.groupby('geo').owner_outright_5564.first()
cy['own_std'] = cy.geo.map((own - own.mean()) / own.std(ddof=0))
bmap = {'G_old': ['A5564', 'AW2554', 'AM2554'], 'G_oldW': ['AW2554'], 'G_oldM': ['AM2554']}
LOG = []
def brs_of(*names):
    out = []
    for n in names:
        for m in bmap.get(n, [n]):
            if m in brk: out.append(brk[m])
            elif m + '__breaks' in cy:
                out.append({g: list(b) for g, b in cy.groupby('geo')[m + '__breaks'].first().items()})
    out += [brk['AW6064']] if n == 'G_oldW' else []
    return out
def run(y, x, controls, tag, side=0, **kw):
    r = fit(cy, y, x, controls, brs_of(y, x, *controls) + ([brk['AW6064']] if y == 'G_oldW' else []) + ([brk['AM6064']] if y == 'G_oldM' else []), side=side, **kw)
    LOG.append(dict(tag=tag, y=y, x=x, controls=list(controls), side=side, trend=kw.get('trend', False), **{k: r[k] for k in ['beta', 'se', 'p', 'p_opposite', 'n', 'G', 'G_star', 'mde']}, years=r['years']))
    print(f"{tag:8s} {y:8s} ~ {x:16s} [{','.join(controls)}]{' trend' if kw.get('trend') else ''}: {fmt(r)}")
    return r
for y in ['G_old', 'G_oldW', 'G_oldM']:
    for x in ['logq_hpi_l1', 'logq_l1']:
        run(y, x, ('U',), 'gap')
cy['hpi_own'] = cy.logq_hpi_l1 * cy.own_std
run('G_old', 'hpi_own', ('U', 'logq_hpi_l1'), 'gap_own')
json.dump(LOG, open(os.path.join(OUT, 'speclog_s10.json'), 'w'), indent=1, default=float)
print('specs', len(LOG))
