"""Where is retirement in the inactivity-reason tables? lfsa_igar (prefetched) asks the main reason only of persons
who want to work, so it has no retirement category; lfsa_igaww splits 55-64 inactivity into want / do not want work;
lfso_12reasnot (2012 ad hoc module, 50-69) gives reasons for leaving work, one year. For understanding only."""
from common import *
pd.set_option('display.width', 250)
ww = es.clean(data.get('lfsa_igaww', {'sex': 'T'}))
ww = ww[ww.age == 'Y55-64']
p = ww.pivot_table(index=['geo', 'year'], columns='wstatus', values='value')
popt = es.clean(extra('pop'))
popt = popt[popt.sex == 'T'].copy()
popt['a'] = popt.age.map(lambda a: 100 if a == 'Y_OPEN' else (0 if a == 'Y_LT1' else int(a[1:])))
p5564 = popt[(popt.a >= 55) & (popt.a <= 64)].groupby(['geo', 'year']).value.sum() / 1000
p['nwant_pct_pop'] = 100 * p['NSEEK_NWANT'] / p5564.reindex(p.index)
p['want_pct_pop'] = 100 * p['NSEEK_WANT'] / p5564.reindex(p.index)
p['nwant_share_inact'] = 100 * p['NSEEK_NWANT'] / p['TOTAL']
t = p.reset_index()
print(t[t.year.isin([2006, 2012, 2019, 2024])].pivot_table(index='geo', columns='year', values=['nwant_pct_pop', 'want_pct_pop', 'nwant_share_inact']).round(1).to_string())
m = es.clean(data.get('lfso_12reasnot', {'sex': 'T'}))
print(m.pivot_table(index='geo', columns='ynlfs', values='value').round(1).to_string())
t.to_csv(os.path.join(OUT, 'inactive_5564_want.csv'), index=False)
