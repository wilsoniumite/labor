# Country-by-country slope of enrolment 20-24 on last year's U 25-54 (OLS on the country's own years, with its own
# break dummies; descriptive), against F_c. Figure: fig_enrol_cycle_by_country.png.
from youth import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
v, cl = man()
v['U2554_l1'] = shift(*v['U2554'], 1)
df, br = frame({k: v[k] for k in ['educ2024', 'U2554_l1']}, years=range(1997, 2026))
bb = union(br['educ2024'], br['U2554_l1'])
rows = []
for g in data.GEOS:
    d = df[df.geo == g].dropna().reset_index(drop=True)
    B = break_dummies(d, {g: bb.get(g, [])})
    X = np.column_stack([np.ones(len(d)), d.U2554_l1, B])
    b, *_ = np.linalg.lstsq(X, d.educ2024.to_numpy(float), rcond=None)
    rows.append(dict(geo=g, slope=b[1], n=len(d), sdU=d.U2554_l1.std(), F_raw=cl.F_raw.get(g)))
T = pd.DataFrame(rows).set_index('geo').sort_values('F_raw'); print(T.round(2))
print('spearman slope vs F_raw:', round(T.slope.corr(T.F_raw, method='spearman'), 2))
T.to_csv('explore/youth_school/enrol_cycle_by_country.csv')
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.scatter(T.F_raw, T.slope)
for g, r in T.iterrows():
    if pd.notna(r.F_raw): ax.annotate(g, (r.F_raw, r.slope), fontsize=8)
ax.axhline(0, color='grey', lw=.5); ax.set_xlabel('F: % of 25-34 living with parents, first years 2003-08')
ax.set_ylabel('pp of 20-24 in education per pp of U25-54 (t-1)')
ax.set_title('Enrolment response to last year\'s prime-age unemployment, by country', fontsize=9)
plt.tight_layout(); plt.savefig('explore/youth_school/fig_enrol_cycle_by_country.png', dpi=90)
