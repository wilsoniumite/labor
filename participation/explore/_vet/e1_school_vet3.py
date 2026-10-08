# Which break dummies carry E1 (stated version)? Diagnostic only: C3 is mechanical and frozen.
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), 'explore', 'youth_school'))
from youth import *          # noqa
import build, data
r = raw()
U = build._by_country(cell(r['une'], age='Y25-54'), cell(r['une_lfs'], age='Y25-54'), data.GEOS)
ed = cell(r['educ'])
v = {'educ2024': ed, 'U2554_l1': build._shift(*U, 1)}
df, br = frame(v, years=range(1997, 2026))
only21 = {g: [y for y in ys if y in (2021, 2022)] for g, ys in union(br['educ2024'], br['U2554_l1']).items()}
no21 = {g: [y for y in ys if y not in (2021, 2022)] for g, ys in union(br['educ2024'], br['U2554_l1']).items()}
for lbl, b in (('only the 2021/22 breaks', only21), ('all breaks but 2021/22', no21)):
    reg(lbl, df, Breaks({'educ2024': b, 'U2554_l1': {}}), 'educ2024', 'U2554_l1', B=1999, log=False)
