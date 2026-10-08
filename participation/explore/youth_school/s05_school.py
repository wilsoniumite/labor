# Schooling as an exit: formal education 20-24 on labour prospects and on q x floor availability.
from youth import *
v, cl = man()
F = cl['F_c']
keys = ['educ2024', 'U2554', 'UL2554', 'E2024_l1', 'logq_l1', 'U', 'UL', 'E2024', 'E2554']
df, br = frame({k: v[k] for k in keys}, years=range(1997, 2026))
df['F'] = df.geo.map(F)
df['QF'] = df.logq_l1 * df.F; br.alias('QF', 'logq_l1')
df['post'] = (df.year >= 2023).astype(float)
R = {}
R['S1'] = reg('S1 educ2024 ~ U2554 (C-6 replica)', df, br, 'educ2024', 'U2554', side=1)
R['S2'] = reg('S2 educ2024 ~ UL2554 (lfsa_urgan, all countries)', df, br, 'educ2024', 'UL2554', side=1)
R['S3'] = reg('S3 educ2024 ~ E2024_l1', df, br, 'educ2024', 'E2024_l1', side=-1)
R['S4'] = reg('S4 educ2024 ~ U2554 + country trends', df, br, 'educ2024', 'U2554', side=1, trends=True)
R['S5'] = reg('S5 educ2024 ~ UL2554 + country trends', df, br, 'educ2024', 'UL2554', side=1, trends=True)
R['S6'] = reg('S6 educ2024 ~ logq_l1 x F | logq_l1, U2554', df.dropna(subset=['F']), br, 'educ2024', 'QF', ['logq_l1', 'U2554'], side=1)
R['S7'] = reg('S7 educ2024 ~ logq_l1 | U2554', df, br, 'educ2024', 'logq_l1', ['U2554'], side=-1)
