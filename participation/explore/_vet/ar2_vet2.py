"""E-AR2 vet, part 2: the lead check on a matched sample, and drop-SE with breaks held."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ['VB'] = '1999'
src = open(os.path.join(HERE, 'ar2_vet.py')).read().split("LOG = {}")[0]
exec(src); C = ('U', 'logq_hpi_l1')
d = cy.dropna(subset=['hpi_f1']).copy()
for tag, x, ctl in [('main_on_lead_sample', 'hpi_own', C), ('lead_only_same', 'hpi_f1_own', ('U', 'hpi_f1')), ('both', 'hpi_own', C + ('hpi_f1', 'hpi_f1_own')), ('both_lead_coef', 'hpi_f1_own', C + ('hpi_f1', 'hpi_own'))]:
    r = fit(d, 'G_old', x, ctl, BR, side=+1, B=1999); print(f"{tag:22s}", fmt(r))
# corr between lag and lead interaction (within, after FE)
d2 = d.dropna(subset=['G_old', 'U', 'hpi_own', 'hpi_f1_own'])
print('corr lag/lead interactions', np.corrcoef(d2.hpi_own, d2.hpi_f1_own)[0, 1])
