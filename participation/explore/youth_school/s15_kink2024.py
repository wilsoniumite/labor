# The floor kink at 20-24 (D1's equation with E 20-24): robustness on the explore half.
from youth import *
v, cl = man()
keys = ['E2024', 'E2024_all', 'E2024M', 'E2024F', 'logq_l1', 'U']
df, br = frame({k: v[k] for k in keys}, years=range(1997, 2026))
df['F'] = df.geo.map(cl['F_c']); d = df.dropna(subset=['F']).copy()
d['QF'] = d.logq_l1 * d.F; br.alias('QF', 'logq_l1')
reg('K1 E2024 ~ q x F | q, U, country trends', d, br, 'E2024', 'QF', ['logq_l1', 'U'], side=-1, trends=True)
reg('K2 E2024_all ~ q x F | q, U', d, br, 'E2024_all', 'QF', ['logq_l1', 'U'], side=-1)
reg('K3 E2024M ~ q x F | q, U', d, br, 'E2024M', 'QF', ['logq_l1', 'U'], side=-1)
reg('K4 E2024F ~ q x F | q, U', d, br, 'E2024F', 'QF', ['logq_l1', 'U'], side=-1)
loo = {}
for g in sorted(set(d.geo)):
    r = reg(f'LOO N3 drop {g}', d[d.geo != g], br, 'E2024', 'QF', ['logq_l1', 'U'], side=-1, log=False, B=1999)
    loo[g] = (round(r['beta'], 2), round(r['p'], 3))
print('LOO N3:', loo)
