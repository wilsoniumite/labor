# Entrants since 2023 against the clerical exposure GAP (share of ISCO 4 in employment at 15-24 minus at 15-64,
# mean 2018-2019; derivations P5), C-4's window. Standardised over the 16 countries.
from youth import *
v, cl = man()
occ = raw()['occ']
def share(age, oc, yrs):
    d = occ[(occ.age == age) & occ.year.isin(yrs) & (occ.sex == 'T')]
    d = d.assign(value=np.where(d.flag.fillna('').str.contains('u|c'), np.nan, d.value))
    p = d.pivot_table(index=['geo', 'year'], columns='isco08', values='value')
    return (p[oc] / p['TOTAL'] * 100).groupby('geo').mean()
gap = share('Y15-24', 'OC4', [2018, 2019]) - share('Y15-64', 'OC4', [2018, 2019])
print('exposure gap (pp):', gap.round(1).to_dict())
Xg = (gap - gap.mean()) / gap.std(ddof=0)
keys = ['gapU', 'educ2024', 'gapE', 'notEnotS2024', 'U']
df, br = frame({k: v[k] for k in keys}, years=[2016, 2017, 2018, 2019, 2022, 2023, 2024, 2025])
df['Xpost'] = df.geo.map(Xg) * (df.year >= 2023); br.alias('Xpost')
out = {}
out['X1'] = reg('X1 gapU ~ gapOC4 x post | U', df, br, 'gapU', 'Xpost', ['U'], side=1)
out['X2'] = reg('X2 educ2024 ~ gapOC4 x post | U', df, br, 'educ2024', 'Xpost', ['U'], side=1)
out['X3'] = reg('X3 gapE ~ gapOC4 x post | U', df, br, 'gapE', 'Xpost', ['U'], side=-1)
out['X4'] = reg('X4 notEnotS2024 ~ gapOC4 x post | U', df, br, 'notEnotS2024', 'Xpost', ['U'], side=1)
d2 = df[df.geo != 'MT']
for k, (y, s) in {'X1m': ('gapU', 1), 'X2m': ('educ2024', 1), 'X4m': ('notEnotS2024', 1)}.items():
    reg(f'{k} {y} ~ gapOC4 x post | U, without MT (check)', d2, br, y, 'Xpost', ['U'], side=s, log=False)
