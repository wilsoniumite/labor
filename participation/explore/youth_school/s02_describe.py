# Descriptives: cross-country levels of youth activity, schooling, NEET split, coresidence, leaving age.
from common import *
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
ar, er, ur, ne, ed, co, cs, la = (extra(k) for k in ['argan','ergan','urgan','neet','educ','cores','cores_status','leave_age'])
def m(df, years, **sel):
    d = df
    for k, v in sel.items(): d = d[d[k] == v]
    d = d[d.year.isin(years)]
    return d.groupby('geo').value.mean()
P = range(2015, 2020)
T = pd.DataFrame({
 'A1519': m(ar, P, sex='T', age='Y15-19', citizen='TOTAL'),
 'A2024': m(ar, P, sex='T', age='Y20-24', citizen='TOTAL'),
 'E2024': m(er, P, sex='T', age='Y20-24', citizen='TOTAL'),
 'U2024': m(ur, P, sex='T', age='Y20-24'),
 'educ1519': m(ed, P, sex='T', age='Y15-19'),
 'educ2024': m(ed, P, sex='T', age='Y20-24'),
 'educ2529': m(ed, P, sex='T', age='Y25-29'),
 'neet2024': m(ne, P, sex='T', age='Y20-24', wstatus='NEMP'),
 'neetU2024': m(ne, P, sex='T', age='Y20-24', wstatus='UNE'),
 'neetI2024': m(ne, P, sex='T', age='Y20-24', wstatus='INAC'),
 'neetIwant': m(ne, P, sex='T', age='Y20-24', wstatus='WANT'),
 'cores1824': m(co, P, sex='T', age='Y18-24'),
 'cores2534': m(co, P, sex='T', age='Y25-34'),
 'leave_age': m(la, P, sex='T'),
 'stud_wp': m(cs, P, wstatus='EDUC', age='Y18-24'),
 'une_wp': m(cs, P, wstatus='UNE', age='Y18-34'),
 'inac_wp': m(cs, P, wstatus='INAC_OTH', age='Y18-34'),
 'empft_wp': m(cs, P, wstatus='EMP_FT', age='Y18-34'),
})
T['inac_share_neet'] = T.neetI2024 / T.neet2024
print(T.round(1).sort_values('cores2534'))
print('\ncross-country correlations (2015-19 means, 16 countries):')
print(T.corr().round(2)[['cores2534','cores1824','leave_age','inac_share_neet','educ2024']])
T.to_csv('explore/youth_school/xsec_2015_2019.csv')
