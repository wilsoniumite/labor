# port_fidelity.py — usage, from pinning/: python3 docs/rewrite/tools/port_fidelity.py paper/main.tex paper/main_rewrite.tex
# Port fidelity: every paragraph whose provenance comment claims "verbatim" (and not "edited") must appear in
# main.tex word for word (whitespace-normalized). For all other paragraphs, list sentences absent from main.tex.
import re, sys, json
OLD = open(sys.argv[1], encoding='utf-8').read()   # main.tex
NEW = open(sys.argv[2], encoding='utf-8').read()   # main_rewrite.tex
def norm(s):
    s = re.sub(r'(?<!\\)%.*', '', s)
    s = s.replace('~', ' ')
    return re.sub(r'\s+', ' ', s).strip()
OLDN = norm(OLD)
lines = NEW.split('\n')
blocks = []  # (prov, start_line, text)
prov, cur, start = [], [], None
def flush():
    global cur, start
    if cur and ''.join(cur).strip():
        blocks.append((' '.join(prov), start, '\n'.join(cur)))
    cur, start = [], None
pending_prov = []
for i, L in enumerate(lines, 1):
    if re.match(r'^\s*%', L):
        if cur: flush(); prov = []
        pending_prov.append(L.strip().lstrip('%').strip())
        continue
    if not L.strip():
        if cur: flush()
        continue
    if pending_prov:
        prov = pending_prov; pending_prov = []
    if start is None: start = i
    cur.append(L)
flush()
def sentences(t):
    t = norm(t)
    # protect common abbreviations
    t2 = re.sub(r'\b(e\.g|i\.e|cf|et al|Prop|Eq|Fig|Sec|vs|U\.S)\.', lambda m: m.group(0).replace('.', '§'), t)
    parts = re.split(r'(?<=[.?!])\s+(?=[A-Z\\(`])', t2)
    return [p.replace('§', '.') for p in parts if len(p.split()) >= 4]
report = {'verbatim_violations': [], 'counts': {}}
for p, start, text in blocks:
    pl = p.lower()
    mixed = 'verbatim' in pl and 'new' in pl.split('verbatim', 1)[1]   # "verbatim ...; then NEW", "the display is NEW"
    cls = ('verbatim' if 'verbatim' in pl and 'edited' not in pl and 'restat' not in pl and 'review edit' not in pl
           and not mixed and not pl.startswith('new')
           else 'edited' if 'edited' in pl or 'restat' in pl or 'review edit' in pl else 'new' if pl.startswith('new') else 'other')
    sents = [x for x in sentences(text) if not x.lstrip().startswith(('\\section', '\\subsection'))]
    missing = [s for s in sents if s not in OLDN]
    c = report['counts'].setdefault(cls, [0, 0])
    c[0] += len(sents); c[1] += len(missing)
    if cls == 'verbatim' and missing:
        report['verbatim_violations'].append({'line': start, 'prov': p[:160], 'missing': [m[:300] for m in missing]})
    if cls == 'other' and missing:
        report.setdefault('other_missing', []).append({'line': start, 'prov': p[:160], 'missing': [m[:200] for m in missing][:3]})
print(json.dumps(report['counts'], indent=1))
print('verbatim-claimed paragraphs with non-verbatim sentences:', len(report['verbatim_violations']))
for v in report['verbatim_violations']:
    print('\nL%d  [%s]' % (v['line'], v['prov']))
    for m in v['missing']: print('   -', m)
print('\nunclassified paragraphs with sentences absent from main.tex:', len(report.get('other_missing', [])))
for v in report.get('other_missing', []):
    print('\nL%d  [%s]' % (v['line'], v['prov']))
    for m in v['missing']: print('   -', m)
