# youth.py — the youth series used in this theme. MAN: built from the frozen manifest's raw frames only (E-eligible);
# EXT: from the extra series (understanding only).
from common import *

def man():
    r = raw()
    act, emp = r['act'], r['emp']
    v = {}
    for cz, suf in (('NAT', ''), ('TOTAL', '_all')):
        v['A2529' + suf] = band(act, [dict(sex=s, age='Y25-29', citizen=cz) for s in 'MF'])
        v['A2529M' + suf] = cell(act, sex='M', age='Y25-29', citizen=cz)
        v['A2529F' + suf] = cell(act, sex='F', age='Y25-29', citizen=cz)
        v['E2529' + suf] = band(emp, [dict(sex=s, age='Y25-29', citizen=cz) for s in 'MF'])
        v['E2024M' + suf] = cell(emp, sex='M', age='Y20-24', citizen=cz)
        v['E2024F' + suf] = cell(emp, sex='F', age='Y20-24', citizen=cz)
    cy, cl = panel()
    for c in [c for c in cy.columns if not c.endswith('__breaks')]:
        s = cy[c]
        b = {}
        for (g, y), bl in cy[c + '__breaks'].items():
            if len(bl):
                b[g] = sorted(set(b.get(g, [])) | set(int(t) for t in bl))
        v[c] = (s, b)
    # C7-style lfsa_urgan for every country (the long-window cycle; never spliced)
    for name, age in (('UL', 'Y25-74'), ('UL2554', 'Y25-54'), ('UL1529', 'Y15-29')):
        v[name] = cell(r['une_lfs'], age=age)
    # derived
    v['nonemp_inac2529'] = combine(lambda a, e: (100 - a) / (100 - e) * 100, v['A2529'], v['E2529'])
    v['U2529_pop'] = combine(lambda a, e: a - e, v['A2529'], v['E2529'])
    v['I2529'] = combine(lambda a: 100 - a, v['A2529'])
    v['gapE'] = combine(lambda a, b: a - b, v['E2024'], v['E2554'])
    v['gapU'] = combine(lambda a, b: a - b, v['U1529'], v['U2554'])
    v['gapUL'] = combine(lambda a, b: a - b, v['UL1529'], v['UL2554'])
    v['E2024_l1'] = shift(*v['E2024'], 1)
    v['notEnotS2024'] = combine(lambda e, s: 100 - e - s, v['E2024'], v['educ2024'])
    v['stud1824_share_of_cores'] = cell(r['stud'])
    return v, cl

def ext():
    ar, er, ur, ne, ed, co, cs, la = (extra(k) for k in ['argan','ergan','urgan','neet','educ','cores','cores_status','leave_age'])
    v = {}
    for a in ['Y15-19', 'Y20-24', 'Y25-29']:
        t = a.replace('Y', '').replace('-', '')
        for s in 'MFT':
            v[f'xA{t}{s}'] = cell(ar, sex=s, age=a, citizen='TOTAL')
            v[f'xE{t}{s}'] = cell(er, sex=s, age=a, citizen='TOTAL')
        v[f'xeduc{t}'] = cell(ed, sex='T', age=a)
    v['xU2024'] = cell(ur, sex='T', age='Y20-24')
    for a in ['Y20-24', 'Y25-29']:
        t = a.replace('Y', '').replace('-', '')
        for w in ['NEMP', 'UNE', 'INAC', 'WANT', 'NWANT']:
            v[f'xneet{w}{t}'] = cell(ne, sex='T', age=a, wstatus=w)
        v[f'xinacshare{t}'] = combine(lambda i, n: i / n * 100, v[f'xneetINAC{t}'], v[f'xneetNEMP{t}'])
    for a in ['Y18-24', 'Y25-34', 'Y20-24', 'Y25-29']:
        v['xcores' + a.replace('Y', '').replace('-', '')] = cell(co, sex='T', age=a)
    v['xleave'] = cell(la, sex='T')
    return v
