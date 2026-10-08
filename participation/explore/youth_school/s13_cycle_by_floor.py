# Does the floor change how the young absorb the cycle? Enrolment and youth unemployment on U25-54 x F_c.
from youth import *
v, cl = man()
v['U2554_l1'] = shift(*v['U2554'], 1)
keys = ['educ2024', 'U2554_l1', 'U1529', 'U2554', 'E2024', 'I2529', 'U2529_pop']
df, br = frame({k: v[k] for k in keys}, years=range(1997, 2026))
df['F'] = df.geo.map(cl['F_c']); d = df.dropna(subset=['F'])
d['ULF'] = d.U2554_l1 * d.F; br.alias('ULF', 'U2554_l1')
d['UF'] = d.U2554 * d.F; br.alias('UF', 'U2554')
reg('C1 educ2024 ~ U2554_l1 x F | U2554_l1', d, br, 'educ2024', 'ULF', ['U2554_l1'], side=1)
reg('C2 U1529 ~ U2554 x F | U2554', d, br, 'U1529', 'UF', ['U2554'], side=-1)
reg('C3 I2529 (inactive 25-29) ~ U2554 x F | U2554', d, br, 'I2529', 'UF', ['U2554'], side=1)
