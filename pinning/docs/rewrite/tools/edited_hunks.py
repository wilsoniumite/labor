# edited_hunks.py — usage, from pinning/: python3 docs/rewrite/tools/edited_hunks.py paper/main.tex paper/main_rewrite.tex
# For paragraphs whose provenance says "from main.tex L<n>[-m] ... edited", word-diff against those main.tex lines and
# print each changed hunk. A hunk whose new words do not appear in the provenance comment is marked UNLISTED.
import re, sys, difflib
OLDL = open(sys.argv[1], encoding='utf-8').read().split('\n')   # main.tex
NEW = open(sys.argv[2], encoding='utf-8').read().split('\n')   # main_rewrite.tex
def norm(s):
    s = re.sub(r'(?<!\\)%.*', '', s); s = s.replace('~', ' ')
    return re.sub(r'\s+', ' ', s).strip()
blocks, prov, pending, cur, start = [], [], [], [], None
for i, L in enumerate(NEW, 1):
    if re.match(r'^\s*%', L):
        if cur: blocks.append((prov, start, cur)); cur, start = [], None
        pending.append(L.strip().lstrip('%').strip()); continue
    if not L.strip():
        if cur: blocks.append((prov, start, cur)); cur, start = [], None
        continue
    if pending: prov, pending = pending, []
    if start is None: start = i
    cur.append(L)
if cur: blocks.append((prov, start, cur))
seen = set(); nunl = 0; nh = 0
for prov, start, cur in blocks:
    p = ' '.join(prov)
    m = re.match(r'from main\.tex L(\d+)(?:\s*[-–]\s*L?(\d+))?', p)
    if not m or 'edited' not in p.lower(): continue
    key = (p, start)
    a = int(m.group(1)); b = int(m.group(2) or a)
    old = norm(' '.join(OLDL[a-1:b])).split(' ')
    new = norm(' '.join(cur)).split(' ')
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    hunks = [(t, ' '.join(old[i1:i2]), ' '.join(new[j1:j2])) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal']
    # ignore hunks where the paragraph is a sub-part of the old lines (pure deletions at ends)
    out = []
    for t, o, n in hunks:
        if t == 'delete' and len(o.split()) > 25: continue  # sentences of the source lines ported elsewhere
        if t == 'insert' and len(n.split()) > 25: n_flag = 'LONG-INSERT'
        else: n_flag = ''
        nw = [w for w in re.findall(r'[A-Za-z]{4,}', n)]
        listed = all(w.lower() in p.lower() for w in nw) if nw else True
        flag = '' if listed else 'UNLISTED'
        if flag: nunl += 1
        nh += 1
        out.append(f'   [{t}{" "+flag if flag else ""}{" "+n_flag if n_flag else ""}] "{o[:150]}" -> "{n[:150]}"')
    if out:
        print(f'\nL{start} (main.tex L{a}-{b}) :: {p[:220]}')
        print('\n'.join(out))
print(f'\n{nh} hunks, {nunl} with new words not named in the provenance comment', file=sys.stderr)
