import sys, os
sys.path.insert(0, 'explore'); sys.path.insert(0, 'code')
import data
import pandas as pd
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
cy, cl = data.panel()
print(cy.columns.tolist()); print(cy.shape); print(cy.head())
print(cl)
raw = data.manifest_raw()
for k, v in raw.items():
    print(k, type(v), getattr(v, 'shape', None)); 
    if hasattr(v, 'columns'): print(v.columns.tolist()); print(v.head(3))
