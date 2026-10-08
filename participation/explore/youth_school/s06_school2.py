# Schooling: is the lagged-youth-employment result mechanical (enrolment persistence)? Prime-age prospects instead.
from youth import *
v, cl = man()
v['E2554_l1'] = shift(*v['E2554'], 1)
v['educ2024_l1'] = shift(*v['educ2024'], 1)
v['U2554_l1'] = shift(*v['U2554'], 1)
v['UL2554_l1'] = shift(*v['UL2554'], 1)
keys = ['educ2024', 'educ2024_l1', 'U2554', 'U2554_l1', 'UL2554_l1', 'E2024_l1', 'E2554_l1', 'U']
df, br = frame({k: v[k] for k in keys}, years=range(1997, 2026))
reg('S8 educ2024 ~ E2554_l1', df, br, 'educ2024', 'E2554_l1', side=-1)
reg('S9 educ2024 ~ E2024_l1 | educ2024_l1 (diagnostic)', df, br, 'educ2024', 'E2024_l1', ['educ2024_l1'], side=-1)
reg('S10 educ2024 ~ U2554_l1', df, br, 'educ2024', 'U2554_l1', side=1)
reg('S11 educ2024 ~ UL2554_l1', df, br, 'educ2024', 'UL2554_l1', side=1)
