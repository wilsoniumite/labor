import sys
sys.path.insert(0, 'explore'); sys.path.insert(0, 'code')
import data
import pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 200)
ig = data.extra('igar')
a = ig[(ig.age == 'Y55-64') & (ig.sex == 'T')]
p = a.pivot_table(index=['geo', 'year'], columns='reason', values='value')
p['SUM'] = p.drop(columns=[c for c in ['FAM_CARE_PER_OTH','FAM_PER_OTH','PER_OTH'] if c in p]).sum(1)
ar = data.extra('argan')
t = ar[(ar.age == 'Y55-64') & (ar.sex == 'T') & (ar.citizen == 'TOTAL')].set_index(['geo', 'year'])['value']
p['INACT'] = 100 - t.reindex(p.index)
print(p.loc[(slice(None), [2006, 2015, 2024]), :].round(1))
print(ig.groupby('reason').year.agg(['min','max','count']))
