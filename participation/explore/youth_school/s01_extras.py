import sys
sys.path.insert(0, 'explore'); sys.path.insert(0, 'code')
import data
import pandas as pd
for k in ['argan','ergan','urgan','igar','neet','educ','cores','cores_status','leave_age','occ']:
    d = data.extra(k)
    print('=====', k, d.shape, d['year'].min(), d['year'].max())
    for c in d.columns:
        if c not in ('geo','year','value','flag'):
            print('  ', c, sorted(d[c].dropna().unique().tolist())[:30])
