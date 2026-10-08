# Entrants since 2023, common shift: youth-minus-prime gaps predicted from the cycle on 2012-2019 (country intercepts,
# common slope on U 25-54), residuals in 2022-2025. Descriptive; the year effect is not identified against other shocks.
from youth import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
v, cl = man(); x = ext()
v['ratioU'] = combine(lambda a, b: a / b, v['U1529'], v['U2554'])
v['xU2024'] = x['xU2024']
v['gapU2024'] = combine(lambda a, b: a - b, x['xU2024'], v['UL2554'])
keys = ['gapU', 'ratioU', 'gapE', 'U2554', 'UL2554', 'gapU2024', 'educ2024']
df, br = frame({k: v[k] for k in keys}, years=range(2012, 2026))
out = {}
fig, axs = plt.subplots(1, 4, figsize=(18, 4))
for ax, (y, u) in zip(axs, [('gapU', 'U2554'), ('ratioU', 'U2554'), ('gapE', 'U2554'), ('gapU2024', 'UL2554')]):
    d = df.dropna(subset=[y, u]).copy()
    pre = d[d.year <= 2019]
    Zp = np.column_stack([inf.fe_matrix(pre, 'geo'), pre[u], np.ones(len(pre))])
    b, *_ = np.linalg.lstsq(Zp, pre[y].to_numpy(float), rcond=None)
    Za = np.column_stack([inf.fe_matrix(d, 'geo'), d[u], np.ones(len(d))])
    d['res'] = d[y] - Za @ b
    m = d.groupby('year').res.agg(['mean', 'count'])
    piv = d.pivot(index='geo', columns='year', values='res')
    print(y, 'slope on', u, round(b[-2], 3)); print(m.round(2).T)
    print('  countries with 2023-25 mean residual > 0:', int((piv[[2023, 2024, 2025]].mean(axis=1) > 0).sum()), 'of', piv[[2023, 2024, 2025]].mean(axis=1).notna().sum())
    for g in piv.index: ax.plot(piv.columns, piv.loc[g], color='lightgrey', lw=.8)
    ax.plot(m.index, m['mean'], 'k-o'); ax.axhline(0, color='grey'); ax.set_title(f'{y}: residual from 2012-19 fit on {u}', fontsize=9)
    out[y] = m['mean'].round(3).to_dict()
plt.tight_layout(); plt.savefig('explore/youth_school/fig_common_shift.png', dpi=80)
json.dump({k: {int(a): b for a, b in d.items()} for k, d in out.items()}, open('explore/youth_school/common_shift.json', 'w'), indent=1)
