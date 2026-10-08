# Robustness of the lagged-cycle enrolment result; and the student-independence moderator built properly from extras.
from youth import *
v, cl = man(); x = ext()
v['U2554_l1'] = shift(*v['U2554'], 1)
v['UL2554_l1'] = shift(*v['UL2554'], 1)
v['xcores1824'] = x['xcores1824']
keys = ['educ2024', 'U2554_l1', 'UL2554_l1', 'U2554', 'logq_l1', 'xcores1824', 'stud1824_share_of_cores']
df, br = frame({k: v[k] for k in keys}, years=range(1997, 2026))
reg('S12 educ2024 ~ U2554_l1 + country trends', df, br, 'educ2024', 'U2554_l1', side=1, trends=True)
reg('S13 educ2024 ~ U2554_l1 | U2554 (horse race)', df, br, 'educ2024', 'U2554_l1', ['U2554'], side=1)
reg('S14 educ2024 ~ U2554_l1, 2010-2019 only', df[df.year <= 2019], br, 'educ2024', 'U2554_l1', side=1)
# leave one out (not separate specifications: same equation, sample check)
loo = {}
for g in data.GEOS:
    r = reg(f'LOO S10 drop {g}', df[df.geo != g], br, 'educ2024', 'U2554_l1', side=1, log=False, B=1999)
    loo[g] = (round(r['beta'], 3), round(r['p'], 4))
print('LOO S10:', loo)
loo2 = {}
for g in data.GEOS:
    r = reg(f'LOO S11 drop {g}', df[df.geo != g], br, 'educ2024', 'UL2554_l1', side=1, log=False, B=1999)
    loo2[g] = (round(r['beta'], 3), round(r['p'], 4))
print('LOO S11:', loo2)
json.dump(dict(S10=loo, S11=loo2), open('explore/youth_school/loo_school.json', 'w'), indent=1)
# student independence, built from extras: share of students 18-24 living with parents ~ EDUC share of coresiders
# x coresidence 18-24 / share of 20-24 in formal education (approximate: the educ age band is 20-24, not 18-24).
d = df.copy()
d['stud_wp_rate'] = d['stud1824_share_of_cores'] * d['xcores1824'] / d['educ2024']
pre = d[d.year.between(2003, 2008)].dropna(subset=['stud_wp_rate']).sort_values('year').groupby('geo').head(3).groupby('geo').stud_wp_rate.mean()
print('approx. % of students 18-24 living with parents (first 3 yrs 2003-08):', pre.round(0).to_dict())
I = 1 - (pre / 100).clip(upper=1)
d['I'] = d.geo.map(I); d['QI'] = d.logq_l1 * d.I; br.alias('QI', 'logq_l1')
reg('S15 educ2024 ~ q x I(proper, extras) | q, U2554', d.dropna(subset=['I']), br, 'educ2024', 'QI', ['logq_l1', 'U2554'], side=-1)
