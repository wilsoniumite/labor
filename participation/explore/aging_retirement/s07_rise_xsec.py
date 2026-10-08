"""The rise of 60-64 participation across countries: change 2009->2019 and 2009->2025 against outright ownership at
55-64 (2015-17), house-price growth relative to CPI, rent/goods growth, initial level, and predicted aging."""
from common import *
import pickle
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
P = pickle.load(open(os.path.join(OUT, 'panel.pkl'), 'rb'))
cy, cl = P['cy'], P['cl']
W = cy.set_index(['geo', 'year'])
def at(v, y):
    return W[v].xs(y, level='year')
def near(v, y, alt):
    s = at(v, y)
    return s.fillna(at(v, alt))
X = pd.DataFrame(index=sorted(cy.geo.unique()))
for v in ['AW6064', 'AM6064', 'AW5559', 'AM5559', 'A5564']:
    X['d_' + v + '_0919'] = at(v, 2019) - at(v, 2009)
    X['d_' + v + '_0924'] = near(v, 2024, 2023) - at(v, 2009)
    X[v + '_09'] = at(v, 2009)
X['own'] = cl.owner_outright_5564
X['dhpi_0919'] = at('logq_hpi_l1', 2019) - at('logq_hpi_l1', 2010)   # levels of 2018 minus 2009
X['dq_0919'] = at('logq_l1', 2019) - at('logq_l1', 2010)
X['aging_pred'] = cl.aging_pred
X['stratum'] = cl.stratum
pd.set_option('display.width', 250)
print(X.round(2).to_string())
num = X.drop(columns='stratum')
print(num.corr().loc[['d_A5564_0919', 'd_AW6064_0919', 'd_AM6064_0919', 'd_A5564_0924'],
                     ['own', 'dhpi_0919', 'dq_0919', 'aging_pred', 'A5564_09', 'AW6064_09', 'AM6064_09']].round(2))
fig, ax = plt.subplots(1, 3, figsize=(14, 4.3))
for k, (xv, lab) in enumerate([('own', 'outright owners 55-64, % (2015-17)'), ('dhpi_0919', 'change log(HPI/CPI) 2009-19'),
                                ('A5564_09', 'activity 55-64 in 2009 (%)')]):
    for g, r in X.iterrows():
        ax[k].scatter(r[xv], r['d_A5564_0919'], c='C0'); ax[k].annotate(g, (r[xv], r['d_A5564_0919']), fontsize=8)
    ax[k].set_xlabel(lab); ax[k].grid(alpha=.3)
ax[0].set_ylabel('change in activity 55-64 (nationals, pp), 2009-19')
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig2_rise_xsec.png'), dpi=110)
X.to_csv(os.path.join(OUT, 'rise_xsec.csv'))
