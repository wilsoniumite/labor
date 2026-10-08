"""Build the analysis panel from the frozen manifest's raw frames (+ panel variables), save to CSV."""
from common import *
cy, cl = data.panel()
cy = cy.reset_index()
R = raw()
brk = {}
for age in ['Y55-59', 'Y60-64']:
    for sex in ['M', 'F']:
        nm = f"A{'W' if sex=='F' else 'M'}{age[1:3]}{age[4:6]}"
        s, b = act(age, sex)
        cy[nm] = s.reindex(pd.MultiIndex.from_frame(cy[['geo', 'year']])).to_numpy()
        brk[nm] = b
        s, b = act(age, sex, 'TOTAL')
        cy[nm + '_all'] = s.reindex(pd.MultiIndex.from_frame(cy[['geo', 'year']])).to_numpy()
# outright owner share 55-64 (2015+), as panel and as country mean 2015-2017
own, ob = series(R['tenure'])
cy['own5564'] = own.reindex(pd.MultiIndex.from_frame(cy[['geo', 'year']])).to_numpy()
cy = cy.merge(cl[['owner_outright_5564', 'F_raw', 'stratum', 'aging_pred', 'routine_change']].reset_index(), on='geo', how='left')
# routine share at 15-64 panel and old ratio from pop
occ = R['occ']
oc = {i: series(occ, age='Y15-64', isco08=i) for i in ['OC4', 'OC7', 'OC8', 'TOTAL']}
rs = 100 * (oc['OC4'][0] + oc['OC7'][0] + oc['OC8'][0]) / oc['TOTAL'][0]
cy['routine'] = rs.reindex(pd.MultiIndex.from_frame(cy[['geo', 'year']])).to_numpy()
pop = es.clean(R['pop'])
pop['a'] = pop.age.map(lambda a: 100 if a == 'Y_OPEN' else int(a[1:]))
old = pop[pop.a >= 56].groupby(['geo', 'year']).value.sum()
wk = pop[(pop.a >= 21) & (pop.a <= 55)].groupby(['geo', 'year']).value.sum()
o65 = pop[pop.a >= 65].groupby(['geo', 'year']).value.sum()
w2064 = pop[(pop.a >= 20) & (pop.a <= 64)].groupby(['geo', 'year']).value.sum()
cnt = pop.groupby(['geo', 'year']).value.count()
ok = cnt[cnt == len(pop.age.unique())].index
cy['oldratio'] = (old / wk).reindex(ok).reindex(pd.MultiIndex.from_frame(cy[['geo', 'year']])).to_numpy()
cy['oadr'] = (o65 / w2064).reindex(ok).reindex(pd.MultiIndex.from_frame(cy[['geo', 'year']])).to_numpy()
import pickle
pickle.dump(dict(cy=cy, brk=brk, cl=cl), open(os.path.join(OUT, 'panel.pkl'), 'wb'))
print(cy.columns.tolist())
print(cy[cy.year.isin([2011, 2019, 2025])][['geo', 'year', 'AW6064', 'AM6064', 'own5564', 'logq_l1', 'logq_hpi_l1', 'routine', 'oldratio']].round(3).to_string())
print(cl.round(3).to_string())
