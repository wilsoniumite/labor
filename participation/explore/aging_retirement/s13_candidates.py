"""The candidate E-hypotheses, estimated once each on the explore half in their final form (one-sided, B=9999),
with leave-one-country-out and the MDE on 15 clusters (explore se)."""
from common import *
import pickle, json
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, cl = P['cy'].copy(), P['cl']
W = cy.set_index(['geo', 'year'])
out = {}
def xsec(name, d, y, x, side):
    d = d.dropna(subset=[y, x]).reset_index()
    Z = inf.fe_matrix(d, ['stratum'])
    r = inf.wcr(d[y].to_numpy(), d[x].to_numpy(), Z, d.geo.to_numpy(), side=side, B=9999)
    loo = {}
    for g in d.geo:
        dd = d[d.geo != g]
        rr = inf.wcr(dd[y].to_numpy(), dd[x].to_numpy(), inf.fe_matrix(dd, ['stratum']), dd.geo.to_numpy(), side=side, B=1999)
        loo[g] = (round(rr['beta'], 3), round(rr['p'], 3))
    r['mde15'] = inf.mde(r['se'], 15)
    print(name, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k in ['beta', 'se', 't', 'p', 'p_opposite', 'n', 'G', 'G_star', 'mde15']})
    print('   LOO', loo)
    out[name] = dict(r, loo=loo, rows=d[['geo', 'stratum', y, x]].round(4).values.tolist())
# E1: convergence of 55-64 participation, 2009 -> 2019
X = pd.DataFrame(index=cl.index)
X['stratum'] = cl.stratum
X['dA5564'] = W.A5564.xs(2019, level='year') - W.A5564.xs(2009, level='year')
X['A5564_09'] = W.A5564.xs(2009, level='year')
xsec('E1_convergence', X, 'dA5564', 'A5564_09', -1)
# E2: realised aging vs routine change 2011-2019 (varies C-5)
og = cy.pivot_table(index='geo', columns='year', values='oldratio')
X['aging_real'] = og[2019] - og[2011]
X['routine_change'] = cl.routine_change
xsec('E2_real_aging_routine', X, 'routine_change', 'aging_real', +1)
# E3: old-minus-prime gap on log(HPI/CPI)_{t-1} x outright ownership 55-64 (2015-17), FE geo+year, U, breaks
cy['G_old'] = cy.A5564 - (cy.AW2554 + cy.AM2554) / 2
own = cl.owner_outright_5564
cy['hpi_own'] = cy.logq_hpi_l1 * cy.geo.map((own - own.mean()) / own.std(ddof=0))
def bl(n):
    return {g: list(b) for g, b in cy.groupby('geo')[n + '__breaks'].first().items()}
r = fit(cy, 'G_old', 'hpi_own', ('U', 'logq_hpi_l1'), [bl('A5564'), bl('AW2554'), bl('AM2554'), bl('logq_hpi_l1'), bl('U')], side=+1)
r['mde15'] = inf.mde(r['se'], 15)
print('E3_old_gap_hpi_x_own', fmt(r), 'mde15', round(r['mde15'], 3))
out['E3_old_gap_hpi_x_own'] = r
json.dump(out, open(os.path.join(OUT, 'candidates_explore.json'), 'w'), indent=1, default=float)
