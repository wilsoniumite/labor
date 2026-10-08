# The floor at 20-29: form of non-employment vs coresidence; the floor kink (D1's equation) on younger outcomes.
from youth import *
v, cl = man(); x = ext()
v.update({k: x[k] for k in ['xinacshare2024', 'xcores1824', 'xneetINAC2024', 'xneetUNE2024', 'xinacshare2529', 'xcores2529']})
keys = ['xinacshare2024', 'xcores1824', 'xneetINAC2024', 'xneetUNE2024', 'xinacshare2529', 'xcores2529',
        'E2024', 'A2529', 'E2529', 'logq_l1', 'U', 'UL', 'nonemp_inac2529']
df, br = frame({k: v[k] for k in keys}, years=range(1997, 2026))
df['F'] = df.geo.map(cl['F_c']); df['QF'] = df.logq_l1 * df.F; br.alias('QF', 'logq_l1')
d = df.dropna(subset=['F'])
reg('N1 inactive share of NEET 20-24 ~ coresidence 18-24 (extras)', df, br, 'xinacshare2024', 'xcores1824', side=1)
reg('N1b inactive share of NEET 25-29 ~ coresidence 25-29 (extras)', df, br, 'xinacshare2529', 'xcores2529', side=1)
reg('N2 inactive share of NEET 20-24 ~ q x F | q, U (extras)', d, br, 'xinacshare2024', 'QF', ['logq_l1', 'U'], side=1)
reg('N3 E2024 ~ q x F | q, U (D1 eq. at 20-24)', d, br, 'E2024', 'QF', ['logq_l1', 'U'], side=-1)
reg('N4 A2529 ~ q x F | q, U', d, br, 'A2529', 'QF', ['logq_l1', 'U'], side=-1)
reg('N5 E2024 ~ q x F | q, UL (long window)', d, br, 'E2024', 'QF', ['logq_l1', 'UL'], side=-1)
reg('N6 NEET inactive 20-24 (pop %) ~ q x F | q, U (extras)', d, br, 'xneetINAC2024', 'QF', ['logq_l1', 'U'], side=1)
reg('N7 inactive share of non-employed 25-29 ~ q x F | q, U', d, br, 'nonemp_inac2529', 'QF', ['logq_l1', 'U'], side=1)
