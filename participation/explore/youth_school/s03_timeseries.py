# Figures: the youth series by country over time.
from youth import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
v, cl = man(); x = ext()
def W(s): return s[0].unstack('year')
order = cl['F_raw'].sort_values().index.tolist()
order = [g for g in order if g in data.GEOS] + [g for g in data.GEOS if g not in cl['F_raw'].dropna().index]
fig, axs = plt.subplots(4, 4, figsize=(16, 13), sharex=True)
for ax, g in zip(axs.flat, order):
    for k, lab in [('E2024', 'emp 20-24'), ('educ2024', 'educ 20-24'), ('U2554', 'U 25-54 (x3)')]:
        s = W(v[k]).loc[g] if g in W(v[k]).index else None
        if s is None: continue
        s = s * (3 if k == 'U2554' else 1)
        ax.plot(s.index, s.values, label=lab)
    ax.set_title(f"{g} (F_raw {cl.loc[g,'F_raw']:.0f})"); ax.axvline(2022.5, color='grey', lw=.5)
axs.flat[0].legend(fontsize=7)
plt.tight_layout(); plt.savefig('explore/youth_school/fig_ts_emp_educ_U.png', dpi=80)
# gap E2024-E2554 since 2014
G = W(v['gapE']).loc[:, 2014:2025]
print('E2024 - E2554 (NAT), level by year:'); print(G.round(1))
GU = W(v['gapU']).loc[:, 2014:2025]; print('U1529 - U2554:'); print(GU.round(1))
ED = W(v['educ2024']).loc[:, 2014:2025]; print('educ2024:'); print(ED.round(1))
