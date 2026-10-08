"""Long window: U from lfsa_urgan Y25-74 (manifest une_lfs) for every country, so the panel starts in the late 1990s.
Older participation on log q (rent/goods) and log q x outright ownership; and older participation on the old-age
ratio (aging pull, 2011+)."""
from common import *
import pickle, json
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, brk = P['cy'].copy(), P['brk']
R = raw()
ul, ulb = series(R['une_lfs'], age='Y25-74')
cy['U_lfs'] = ul.reindex(pd.MultiIndex.from_frame(cy[['geo', 'year']])).to_numpy()
own = cy.groupby('geo').owner_outright_5564.first()
cy['own_std'] = cy.geo.map((own - own.mean()) / own.std(ddof=0))
LOG = []
def brs_of(*names):
    out = []
    for n in names:
        if n == 'U_lfs': out.append(ulb)
        elif n in brk: out.append(brk[n])
        elif n + '__breaks' in cy:
            out.append({g: list(b) for g, b in cy.groupby('geo')[n + '__breaks'].first().items()})
    return out
def run(y, x, controls, tag, side=0, df=None, **kw):
    df = cy if df is None else df
    r = fit(df, y, x, controls, brs_of(y, x, *controls), side=side, **kw)
    LOG.append(dict(tag=tag, y=y, x=x, controls=list(controls), side=side, trend=kw.get('trend', False), **{k: r[k] for k in ['beta', 'se', 'p', 'p_opposite', 'n', 'G', 'G_star', 'mde']}, years=r['years']))
    print(f"{tag:8s} {y:8s} ~ {x:12s} [{','.join(controls)}]{' trend' if kw.get('trend') else ''}: {fmt(r)}")
cy['logq_l1_own'] = cy.logq_l1 * cy.own_std
for y in ['A5564', 'AW6064', 'AM6064']:
    run(y, 'logq_l1', ('U_lfs',), 'long')
for y in ['A5564', 'AW6064', 'AM6064']:
    run(y, 'logq_l1_own', ('U_lfs', 'logq_l1'), 'long_own')
# aging pull: older participation on old ratio (2011+)
for y in ['A5564', 'AW6064', 'AM6064']:
    run(y, 'oldratio', ('U',), 'agepull')
json.dump(LOG, open(os.path.join(OUT, 'speclog_s08.json'), 'w'), indent=1, default=float)
print('specs', len(LOG))
