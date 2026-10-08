"""Adversarial vet of E-AR1 (convergence of 55-64 activity, 2009->2019), explore half only, manifest frames only.
Run from participation/: ../venv/Scripts/python.exe explore/_vet/ear1_vet.py"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'explore')); sys.path.insert(0, os.path.join(ROOT, 'code'))
import numpy as np, pandas as pd
import data, eurostat as es, inference as inf

R = data.manifest_raw()
act = R['act']
print('act columns', act.columns.tolist(), 'ages', sorted(act.age.unique()), 'years', act.year.min(), act.year.max())
STR = {g: s for s, gs in es.STRATA.items() for g in gs}
c = es.clean(act)
c['year'] = c.year.astype(int)
def band(ages, cz='NAT', sexes=('M', 'F')):
    d = c[(c.citizen == cz) & c.age.isin(ages) & c.sex.isin(sexes)]
    w = d.pivot_table(index=['geo', 'year'], columns=['sex', 'age'], values='value', aggfunc='first')
    need = len(ages) * len(sexes)
    m = w.mean(axis=1)
    m[w.notna().sum(axis=1) < need] = np.nan
    return m
def brk(ages, cz='NAT'):
    d = act[(act.citizen == cz) & act.age.isin(ages)]
    return es.break_years(d)

O = ['Y55-59', 'Y60-64']
P = ['Y25-29', 'Y30-34', 'Y35-39', 'Y40-44', 'Y45-49', 'Y50-54']
A = band(O); AT = band(O, 'TOTAL'); AP = band(P)
nspec = 0
def run(name, y0, y1, s=A, fe=True, side=-1, drop=(), B=9999, loo=False, transform=None):
    global nspec; nspec += 1
    lv0 = s.xs(y0, level='year'); lv1 = s.xs(y1, level='year')
    d = pd.DataFrame({'a0': lv0, 'a1': lv1}).dropna()
    d = d[~d.index.isin(drop)]
    if transform == 'gap':     # log of the distance to 100 (ceiling)
        d['y'] = np.log(100 - d.a0) - np.log(100 - d.a1); d['x'] = d.a0
    elif transform == 'logit':
        lg = lambda p: np.log(p / (100 - p))
        d['y'] = lg(d.a1) - lg(d.a0); d['x'] = lg(d.a0)
    else:
        d['y'] = d.a1 - d.a0; d['x'] = d.a0
    d = d.reset_index().rename(columns={'index': 'geo'})
    d['stratum'] = d.geo.map(STR)
    Z = inf.fe_matrix(d, ['stratum']) if fe else np.zeros((len(d), 0))
    r = inf.wcr(d.y.to_numpy(), d.x.to_numpy(), Z, d.geo.to_numpy(), side=side, B=B)
    out = f"{name:44s} b={r['beta']:+.3f} se={r['se']:.3f} t={r['t']:+.2f} p={r['p']:.4f} G={r['G']} G*={r['G_star']:.1f} mde15={inf.mde(r['se'],15):.3f}"
    if loo:
        ps = {}
        for g in d.geo:
            dd = d[d.geo != g]
            Zd = inf.fe_matrix(dd, ['stratum']) if fe else np.zeros((len(dd), 0))
            rr = inf.wcr(dd.y.to_numpy(), dd.x.to_numpy(), Zd, dd.geo.to_numpy(), side=side, B=1999)
            ps[g] = (round(rr['beta'], 3), round(rr['p'], 3))
        out += '\n   LOO worst: ' + str(sorted(ps.items(), key=lambda kv: -kv[1][1])[:4])
    print(out)
    return r, d

print('\n== reproduce ==')
r0, d0 = run('E-AR1 as proposed', 2009, 2019, loo=True)
print(d0.round(2).to_string())
print('\n== breaks on the 55-64 NAT cells (C3 flags) between 2009 and 2019 ==')
b = brk(O)
print({g: [y for y in ys if 2009 <= y <= 2019] for g, ys in b.items() if any(2009 <= y <= 2019 for y in ys)})
print('\n== spec sensitivity ==')
run('no stratum FE', 2009, 2019, fe=False, loo=True)
for y0, y1 in [(2008, 2019), (2010, 2019), (2009, 2018), (2009, 2024), (2011, 2019), (2006, 2019), (2005, 2015), (2012, 2019), (2014, 2019), (2009, 2014)]:
    try:
        run(f'window {y0}-{y1}', y0, y1)
    except Exception as e:
        print(y0, y1, 'fail', e)
run('all residents (TOTAL)', 2009, 2019, s=AT)
run('ceiling: dlog(100-A) on A09 (side +1? see note)', 2009, 2019, transform='gap', side=-1)
run('logit change on logit level', 2009, 2019, transform='logit')
run('drop breaks countries', 2009, 2019, drop=[g for g, ys in b.items() if any(2010 <= y <= 2019 for y in ys)])
for sx in ['M', 'F']:
    for ag in O:
        run(f'cell {sx} {ag}', 2009, 2019, s=band([ag], sexes=(sx,)))
print('\n== placebo: prime age 25-54 converges too? ==')
run('A2554 convergence 2009-2019', 2009, 2019, s=AP)
print('\n== null calibration: shuffle 2019 levels? persistence slope ==')
d = d0.copy()
print('corr(a0,a1)=%.3f  sd a0=%.2f sd a1=%.2f  slope a1 on a0 (no FE)=%.3f' % (np.corrcoef(d.a0, d.a1)[0, 1], d.a0.std(), d.a1.std(), np.polyfit(d.a0, d.a1, 1)[0]))
print('\n== does the sigma shrink? (sigma convergence) ==')
for y in [2005, 2009, 2014, 2019, 2024]:
    v = A.xs(y, level='year').dropna()
    print(y, 'n', len(v), 'sd %.2f' % v.std(), 'mean %.2f' % v.mean())
print('\n== MDE scaling: se with G=15 drawn from the explore residual var, stratum FE consuming 4 df ==')
print('specs estimated in this vet:', nspec)
