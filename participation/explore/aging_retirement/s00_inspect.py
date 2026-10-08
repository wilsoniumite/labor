import sys, os
sys.path.insert(0, 'explore'); sys.path.insert(0, 'code')
import data
import pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
for k in ['argan', 'igar', 'tenure', 'hpi', 'occ', 'pop', 'hicp', 'comp']:
    d = data.extra(k)
    print('=====', k, d.shape, list(d.columns))
    for c in d.columns:
        if c not in ('value', 'flag', 'year', 'geo') and d[c].nunique() < 60:
            print('  ', c, sorted(d[c].dropna().unique())[:60])
    print('  years', d.year.min(), d.year.max(), 'geos', sorted(d.geo.unique()))
raw = data.manifest_raw()
for k, v in raw.items():
    print('MANIFEST', k, v.shape, (v.year.min(), v.year.max()) if len(v) else None)
