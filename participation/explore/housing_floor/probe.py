import sys, os
sys.path.insert(0, 'explore'); sys.path.insert(0, 'code')
import data
raw = data.manifest_raw()
for k, v in raw.items():
    print(k, v.shape, list(v.columns)[:10], v['year'].min() if len(v) else None, v['year'].max() if len(v) else None)
print(raw['hicp'].head())
for k in ['overburden', 'cores', 'hicp', 'hpi', 'tenure']:
    d = data.extra(k)
    print(k, d.shape, list(d.columns))
    for c in d.columns:
        if c not in ('geo','year','value','flag') and d[c].nunique() < 40:
            print('   ', c, sorted(d[c].dropna().unique())[:40])
