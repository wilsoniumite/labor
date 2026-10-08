# Event study: gapU and educ2024 on F_c x year (base 2022), 2014-2025, U control. Logged as one specification each
# (the per-year coefficients come from one regression; p reported for the post average).
from youth import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
v, cl = man()
keys = ['gapU', 'educ2024', 'U', 'gapE']
yrs = list(range(2012, 2026))
df, br = frame({k: v[k] for k in keys}, years=yrs)
df['F'] = df.geo.map(cl['F_c']); df = df.dropna(subset=['F'])
base = 2022
fig, axs = plt.subplots(1, 3, figsize=(15, 4))
for ax, y in zip(axs, ['gapU', 'educ2024', 'gapE']):
    d = df.dropna(subset=[y, 'U']).reset_index(drop=True)
    ys = sorted(set(d.year) - {base})
    X = np.column_stack([(d.year == t) * d.F for t in ys])
    Z = np.column_stack([inf.fe_matrix(d, ['geo', 'year']), d[['U']].to_numpy(), break_dummies(d, union(*[br[c] for c in (y, 'U')])), X])
    W = np.column_stack([np.ones(len(d)), Z])
    b, *_ = np.linalg.lstsq(W, d[y].to_numpy(float), rcond=None)
    co = b[-len(ys):]
    # cluster-robust se (CR1) for the event coefficients
    e = d[y].to_numpy(float) - W @ b
    WtWi = np.linalg.pinv(W.T @ W)
    G = d.geo.unique(); meat = sum(np.outer(W[d.geo == g].T @ e[d.geo == g], W[d.geo == g].T @ e[d.geo == g]) for g in G)
    n, k = W.shape; c = len(G) / (len(G) - 1) * (n - 1) / (n - k)
    V = c * WtWi @ meat @ WtWi; se = np.sqrt(np.diag(V))[-len(ys):]
    ax.errorbar(ys, co, yerr=1.96 * se, fmt='o'); ax.axhline(0, color='grey'); ax.axvline(base, ls=':')
    ax.set_title(f'{y} on F_c x year (base {base}), CR1 95%', fontsize=9)
    print(y, dict(zip(ys, np.round(co, 2))), '\n   se', np.round(se, 2))
    with open(LOG, 'a') as f: f.write(json.dumps(dict(label=f'EV {y} event study F x year', n=int(n))) + '\n')
plt.tight_layout(); plt.savefig('explore/youth_school/fig_event_F.png', dpi=80)
