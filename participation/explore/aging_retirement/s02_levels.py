"""Older participation 55-59, 60-64, 65-69 by sex, explore half, 1995-2025 (extra argan, NAT)."""
from common import *
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
ar = extra('argan')
rows = []
for age in ['Y55-59', 'Y60-64', 'Y65-69']:
    for sex in ['M', 'F']:
        s, _ = series(ar, age=age, sex=sex, citizen='NAT')
        for (g, y), v in s.items():
            rows.append((g, y, age, sex, v))
L = pd.DataFrame(rows, columns=['geo', 'year', 'age', 'sex', 'v'])
L.to_csv(os.path.join(OUT, 'older_activity_long.csv'), index=False)
tab = L[L.year.isin([2000, 2005, 2009, 2015, 2019, 2025])].pivot_table(index=['age', 'sex', 'geo'], columns='year', values='v')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 300)
print(tab.round(1))
# change 2009 -> 2025 (or latest) by group
fig, axes = plt.subplots(3, 2, figsize=(11, 11), sharex=True, sharey='row')
for i, age in enumerate(['Y55-59', 'Y60-64', 'Y65-69']):
    for j, sex in enumerate(['M', 'F']):
        ax = axes[i, j]
        d = L[(L.age == age) & (L.sex == sex)]
        for g, dd in d.groupby('geo'):
            ax.plot(dd.year, dd.v, lw=1)
            last = dd.sort_values('year').iloc[-1]
            ax.text(last.year + 0.2, last.v, g, fontsize=7)
        m = d.groupby('year').v.mean()
        ax.plot(m.index, m.values, 'k', lw=2.5)
        ax.set_title(f'{age[1:]} {"men" if sex=="M" else "women"} (nationals; black = mean)')
        ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig1_older_activity.png'), dpi=110)
# mean by year for a balanced set
bal = L.pivot_table(index=['age', 'sex', 'year'], columns='geo', values='v')
for (age, sex), d in bal.groupby(level=[0, 1]):
    d = d.droplevel([0, 1])
    ok = d.loc[2005:2025].dropna(axis=1).columns
    print(age, sex, 'balanced n=', len(ok), {y: round(d.loc[y, ok].mean(), 1) for y in [2005, 2009, 2015, 2019, 2025] if y in d.index})
