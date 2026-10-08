# Post-2023 changes by country against floor availability F_c and clerical exposure X_c (descriptive, no regressions).
from youth import *
v, cl = man(); x = ext()
def W(s): return s[0].unstack('year')
def ch(k, src=v, a=(2016, 2017, 2018, 2019), b=(2023, 2024, 2025)):
    w = W(src[k]); return w[[c for c in b if c in w]].mean(1) - w[[c for c in a if c in w]].mean(1)
def ch2(k, src=v):
    w = W(src[k]); return w[[2023, 2024, 2025]].mean(1) - w[2022]
occ = raw()['occ']
def share(age, oc, yrs):
    d = occ[(occ.age == age) & occ.year.isin(yrs) & (occ.sex == 'T')]
    p = d.pivot_table(index=['geo', 'year'], columns='isco08', values='value')
    return (p[oc] / p['TOTAL'] * 100).groupby('geo').mean()
gap4 = share('Y15-24', 'OC4', [2018, 2019]) - share('Y15-64', 'OC4', [2018, 2019])
T = pd.DataFrame({'F_raw': cl.F_raw, 'X_c': cl.X_c, 'gapOC4': gap4,
                  'd_gapE': ch('gapE'), 'd_gapE_22': ch2('gapE'), 'd_E2024': ch('E2024'), 'd_E2554': ch('E2554'),
                  'd_educ': ch('educ2024'), 'd_educ_22': ch2('educ2024'), 'd_gapU': ch('gapU'), 'd_gapU_22': ch2('gapU'),
                  'd_notEnotS': ch('notEnotS2024'),
                  'd_neetU': ch('xneetUNE2024', x), 'd_neetI': ch('xneetINAC2024', x), 'd_A2024': ch('xA2024T', x)})
print(T.round(1).sort_values('F_raw'))
print(T.corr(method='spearman').round(2).loc[['F_raw', 'X_c', 'gapOC4']])
T.to_csv('explore/youth_school/post2023_changes.csv')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3, figsize=(15, 4.5))
for ax, k, lab in zip(axs, ['d_gapE', 'd_educ', 'd_gapU'], ['E20-24 minus E25-54', 'in formal education 20-24', 'U15-29 minus U25-54']):
    ax.scatter(T.F_raw, T[k])
    for g, r in T.iterrows(): ax.annotate(g, (r.F_raw, r[k]), fontsize=8)
    ax.axhline(0, color='grey', lw=.5); ax.set_xlabel('F: share of 25-34 living with parents, first years 2003-08 (%)')
    ax.set_title(f'change, 2023-25 mean minus 2016-19 mean: {lab}', fontsize=9)
plt.tight_layout(); plt.savefig('explore/youth_school/fig_post2023_vs_F.png', dpi=80)
