# Figures for findings.md: the NEET split against coresidence (cross-section) and E1's partial scatter.
from youth import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
T = pd.read_csv('explore/youth_school/xsec_2015_2019.csv', index_col=0)
fig, axs = plt.subplots(1, 2, figsize=(12, 4.5))
for ax, (xk, yk, xl, yl) in zip(axs, [('cores1824', 'inac_share_neet', '% of 18-24 living with parents', 'inactive share of NEET 20-24 (%)'),
                                     ('cores1824', 'neetU2024', '% of 18-24 living with parents', 'unemployed NEET, % of 20-24')]):
    y = T[yk] * (100 if yk == 'inac_share_neet' else 1)
    ax.scatter(T[xk], y)
    for g in T.index: ax.annotate(g, (T.loc[g, xk], y[g]), fontsize=8)
    ax.set_xlabel(xl); ax.set_ylabel(yl)
axs[0].set_title('2015-2019 means, 16 explore countries', fontsize=9)
plt.tight_layout(); plt.savefig('explore/youth_school/fig_neet_split_vs_coresidence.png', dpi=90)
# E1 partial scatter
v, cl = man()
v['U2554_l1'] = shift(*v['U2554'], 1)
df, br = frame({k: v[k] for k in ['educ2024', 'U2554_l1']}, years=range(1997, 2026))
d = df.dropna().reset_index(drop=True)
Z = np.column_stack([np.ones(len(d)), inf.fe_matrix(d, ['geo', 'year']), break_dummies(d, union(br['educ2024'], br['U2554_l1']))])
P = lambda a: a - Z @ np.linalg.lstsq(Z, a, rcond=None)[0]
ry, rx = P(d.educ2024.to_numpy(float)), P(d.U2554_l1.to_numpy(float))
fig, ax = plt.subplots(figsize=(6.5, 4.5))
for g in sorted(set(d.geo)):
    m = (d.geo == g).to_numpy(); ax.scatter(rx[m], ry[m], s=12, label=g)
b = (rx @ ry) / (rx @ rx)
xs = np.linspace(rx.min(), rx.max(), 2); ax.plot(xs, b * xs, 'k-')
ax.set_xlabel('U 25-54 in t-1, net of country, year and break effects (pp)')
ax.set_ylabel('% of 20-24 in formal education, net (pp)')
ax.set_title(f'E1 on the explore half: slope {b:.2f}, n={len(d)}, 16 countries', fontsize=9)
ax.legend(fontsize=6, ncol=2); plt.tight_layout(); plt.savefig('explore/youth_school/fig_E1_partial.png', dpi=90)
print('E1 FWL slope', round(b, 4))
cs = json.load(open('explore/youth_school/common_shift.json'))
print(pd.DataFrame(cs).round(2).T)
