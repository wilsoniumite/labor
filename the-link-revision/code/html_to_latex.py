# html_to_latex.py — generate an Overleaf-ready LaTeX project from paper/pinning.html.
#
# paper/pinning.html stays canonical; latex/main.tex is a generated artifact.
# Re-run after any edit to the HTML:  ../venv/Scripts/python.exe code/html_to_latex.py
#
# Pipeline: SPECIAL literal replacements -> parse HTML to a tree -> walk body blocks
# -> rewrite literal cross-references into \label/\ref pairs -> emit main.tex
# -> verify (word-sequence diff vs the HTML, env/brace balance, numbering
# assertions, every \ref resolves, unicode leftovers). Fails loudly on any
# structural surprise.
#
# Cross-references (added 2026-08-21): every numbered object gets a stable
# \label keyed on its TITLE (sections/appendices), NAME (theorems), FILE
# (figures), or position (equations, register items), and every in-prose
# mention ("Section 4", "Appendix F.3", "Proposition B.2", "Figure 3",
# "Prediction 8", bare "F.1"/"D.1") is rewritten to \ref against the map --
# so reordering in LaTeX renumbers everything automatically. Retitling a
# heading in the HTML fails the run until HEAD_LABELS learns the new title;
# that is deliberate. The word-fidelity check resolves each \ref back to the
# number it prints, so fidelity still holds token-for-token.

from html.parser import HTMLParser
from collections import Counter
import difflib
import pathlib
import re
import shutil
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / 'paper' / 'pinning.html'
OUT = ROOT / 'latex'
FIGSRC = ROOT / 'figures'

FAIL = []


def check(ok, msg):
    print(f'[{"PASS" if ok else "FAIL"}] {msg}')
    if not ok:
        FAIL.append(msg)


# ---------------------------------------------------------------------------
# Cell 1 — SPECIAL literal replacements (raw HTML, before parsing).
# The matrix-recursion displays mix <b> vectors and bare text in ways the generic
# rules cannot see; each becomes a placeholder emitting hand-written LaTeX.

PLACEHOLDER_LATEX = {}


def _ph(n):
    return f'\u25a0PH{n}\u25a0'  # sentinel char never in the paper


SPECIALS = [
    # two occurrences since the 2026-08-27 notation pass bolded Section 10's
    # matrix display to match Appendix A (v2 map: bold produced-price and
    # rent vectors everywhere)
    ('<b>c</b> = <b>Ac</b> + <b>&Lambda;</b><i>w</i> + <b>Br</b>',
     r'$\mathbf{c} = \mathbf{A}\mathbf{c} + \boldsymbol{\Lambda}w + \mathbf{B}\mathbf{r}$', 2),
    ('<b>c</b> = (&#120793;&minus;<b>A</b>)<sup>&minus;1</sup>(<b>&Lambda;</b><i>w</i> + <b>Br</b>)',
     r'$\mathbf{c} = (\mathbbm{1}-\mathbf{A})^{-1}(\boldsymbol{\Lambda}w + \mathbf{B}\mathbf{r})$', 1),
]


def apply_specials(html):
    for n, (snippet, latex, expected) in enumerate(SPECIALS):
        count = html.count(snippet)
        check(count == expected, f'SPECIAL {n}: {expected} occurrence(s), found {count}')
        PLACEHOLDER_LATEX[_ph(n)] = latex
        html = html.replace(snippet, _ph(n))
    return html


# ---------------------------------------------------------------------------
# Cell 2 — HTML -> tree

class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': 'root', 'attrs': {}, 'children': []}
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'children': []}
        self.stack[-1]['children'].append(node)
        if tag not in ('img', 'br', 'meta'):
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1]['children'].append(data)


def parse(html):
    tb = TreeBuilder()
    tb.feed(html)
    return tb.root


def find(node, tag):
    for ch in node['children']:
        if isinstance(ch, dict):
            if ch['tag'] == tag:
                return ch
            got = find(ch, tag)
            if got:
                return got
    return None


def cls(node):
    return node['attrs'].get('class', '')


def text_of(node):
    out = []
    for ch in node['children']:
        out.append(ch if isinstance(ch, str) else text_of(ch))
    return ''.join(out)


# ---------------------------------------------------------------------------
# Cell 3 — character tables

GREEK = {
    '\u03c1': r'\rho', '\u03bb': r'\lambda', '\u03b3': r'\gamma', '\u03c3': r'\sigma',
    '\u03b7': r'\eta', '\u00b5': r'\mu', '\u03bc': r'\mu', '\u03c4': r'\tau',
    '\u03ba': r'\kappa', '\u03c9': r'\omega', '\u03b2': r'\beta', '\u03b5': r'\varepsilon',
    '\u03b8': r'\theta', '\u03b4': r'\delta', '\u03c6': r'\varphi',
    '\u03b1': r'\alpha', '\u03c8': r'\psi', '\u03c0': r'\pi',
    '\u0394': r'\Delta', '\u039b': r'\Lambda',
}
ELL = '\u2113'
ATOMSYM = {                   # standalone symbols that anchor a math run
    '\u2192': r'\to', '\u2193': r'\downarrow', '\u00d7': r'\times', '\u2248': r'\approx',
    '\u2202': r'\partial', '\u222b': r'\int', '\u2205': r'\emptyset', '\u2261': r'\equiv',
    '\u2264': r'\le', '\u2265': r'\ge', '\u2208': r'\in',
    ELL: r'\ell', '\u03a3': r'\sum', '\u0394': r'\Delta',
    '\u221e': r'\infty', '\u22a5': r'\perp', '\U0001d7d9': r'\mathbbm{1}',
    '\u2026': r'\dots',
}
BRIDGEMAP = {                 # connective symbols valid inside a run
    '\u2212': '-', '\u00b7': r'\cdot ',
    '<': ' < ', '>': ' > ', '$': r'\$', '%': r'\%',
}
OPSET = set('=+*/<>') | {'\u2212', '\u00b7'}
BRIDGECH = set('()[]{}=+/,.|') | set('0123456789') | set(BRIDGEMAP)
COMBINING = {'\u0304': r'\bar', '\u0303': r'\tilde', '\u0302': r'\hat',
             '\u0332': r'\underline'}
SUP2 = '\u00b2'
QED = '\u220e'
EMSP = '\u2003'


def esc_text(s):
    s = s.replace('\\', r'\textbackslash{}')
    for a, b in [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_'),
                 ('{', r'\{'), ('}', r'\}'), ('~', r'\textasciitilde{}'),
                 ('^', r'\textasciicircum{}')]:
        s = s.replace(a, b)
    s = s.replace('\u2014', '---').replace('\u2013', '--')
    s = s.replace('\u00a0', '~').replace(EMSP, r'\quad ')
    s = re.sub(r'(^|[\s(\[])"', r'\1``', s)
    s = s.replace('"', "''")
    for ch, cmd in list(ATOMSYM.items()):
        s = s.replace(ch, f'${cmd}$')
    for ch, cmd in BRIDGEMAP.items():
        if ch not in '<>$%':
            s = s.replace(ch, f'${cmd.strip()}$')
    for ch, cmd in GREEK.items():
        s = s.replace(ch, f'${cmd}$')
    s = s.replace(SUP2, r'${}^{2}$')
    return s


def greek_or_letter(chstr, boldctx=False):
    base, marks = chstr[0], chstr[1:]
    if base in GREEK:
        core = GREEK[base]
    elif base == ELL:
        core = r'\ell'
    elif re.fullmatch(r'[A-Za-z]', base):
        core = base
    else:
        return None
    for m in marks:
        if m in COMBINING:
            core = COMBINING[m] + '{' + core + '}'
        else:
            return None
    if boldctx:
        core = r'\bm{' + core + '}'
    return core


def clusters_of(t):
    clusters = []
    for ch in t:
        if unicodedata.combining(ch) and clusters:
            clusters[-1] += ch
        else:
            clusters.append(ch)
    return clusters


def i_math_atom(t, boldctx=False):
    """Classify <i> content: math latex if it is a math atom, else None."""
    t = t.strip()
    if not t:
        return None
    cl = clusters_of(t)
    if len(cl) > 2:
        return None
    if len(cl) == 2 and not all(re.fullmatch(r'[A-Za-z]', c[0]) for c in cl):
        return None
    parts = []
    for c in cl:
        got = greek_or_letter(c, boldctx)
        if got is None:
            return None
        parts.append(got)
    return ' '.join(p for p in parts) if any('\\' in p for p in parts) else ''.join(parts)


# ---------------------------------------------------------------------------
# Cell 4 — inline conversion

def seglist(children, boldctx=False):
    segs = []
    for ch in children:
        if isinstance(ch, str):
            segs.append(('text', ch))
            continue
        tag = ch['tag']
        if tag == 'i':
            inner = text_of(ch)
            atom = i_math_atom(inner, boldctx)
            segs.append(('atom', atom) if atom is not None else ('textit', inner))
        elif tag == 'b':
            inner = text_of(ch).strip()
            if len(clusters_of(inner)) == 1:
                base = inner[0]
                if base in GREEK:
                    segs.append(('atom', r'\boldsymbol{' + GREEK[base] + '}'))
                else:
                    segs.append(('atom', r'\mathbf{' + base + '}'))
            else:
                segs.append(('bold', ch['children']))
        elif tag == 'sub':
            segs.append(('sub', script_math(ch)))
        elif tag == 'sup':
            segs.append(('sup', script_math(ch)))
        elif tag == 'span':
            segs.append(('tagspan' if cls(ch) == 'tag' else 'plainspan', ch['children']))
        elif tag == 'br':
            segs.append(('br', None))
        else:
            raise AssertionError(f'unexpected inline tag <{tag}>')
    return segs


def script_math(node):
    out = []
    for ch in node['children']:
        if isinstance(ch, str):
            for piece in re.findall(r'[A-Za-z]+|[0-9]+|.', ch):
                if piece in GREEK:
                    out.append(GREEK[piece])
                elif piece == '\u2212':
                    out.append('-')
                elif piece.isalpha():
                    out.append(piece if len(piece) == 1 else r'\mathrm{' + piece + '}')
                else:
                    out.append(piece)
        elif ch['tag'] == 'i':
            atom = i_math_atom(text_of(ch))
            assert atom is not None, f'sub/sup <i> not math: {text_of(ch)!r}'
            out.append(atom)
        else:
            raise AssertionError(f'unexpected tag in script: {ch["tag"]}')
    return ''.join(out)


def tokenize_text(s):
    toks = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch.isalpha() and ch not in GREEK and ch not in ATOMSYM and ch != ELL \
                and not unicodedata.combining(ch):
            j = i + 1
            while j < n and unicodedata.combining(s[j]):
                j += 1
            if j > i + 1:  # bare letter carrying a combining accent, e.g. L-bar
                got = greek_or_letter(s[i:j])
                assert got, f'unmapped accented letter {s[i:j]!r}'
                toks.append(('atomsym', got))
                i = j
                continue
            j = i
            while j < n and ((s[j].isalpha() and s[j] not in GREEK and s[j] != ELL) or s[j] == "'"):
                j += 1
            toks.append(('word', s[i:j]))
            i = j
        elif ch in (' ', '\n', '\t', '\u00a0'):
            toks.append(('sp', ' '))
            i += 1
        elif ch in GREEK or ch == ELL or ch in ATOMSYM:
            j = i + 1
            while j < n and unicodedata.combining(s[j]):
                j += 1
            cluster = s[i:j]
            if ch in ATOMSYM and len(cluster) == 1:
                toks.append(('atomsym', ATOMSYM[ch]))
            else:
                got = greek_or_letter(cluster)
                assert got, f'unmapped symbol cluster {cluster!r}'
                toks.append(('atomsym', got))
            i = j
        elif ch == SUP2:
            toks.append(('sup2', None))
            i += 1
        elif ch == '*':
            toks.append(('star', None))
            i += 1
        elif ch in BRIDGECH:
            toks.append(('bridge', ch))
            i += 1
        else:
            toks.append(('other', ch))
            i += 1
    return toks


def flatten_tokens(segs):
    toks = []
    for kind, val in segs:
        if kind == 'text':
            toks.extend(tokenize_text(val))
        else:
            toks.append((kind, val))
    # single letters glued between MATH symbols become atoms: (1-a-...).
    # Punctuation does not glue — "U.S.", "1950s", "(a)" stay text.
    mathglue = set('=+*/<>0123456789') | {'−', '·'}

    def glues(tok):
        k, v = tok
        if k in ('atomsym', 'atom', 'star', 'sup2', 'sub', 'sup'):
            return True
        return k == 'bridge' and v in mathglue

    for idx, (k, v) in enumerate(toks):
        if k == 'word' and len(v) == 1 and v.isalpha():
            prev = toks[idx - 1] if idx > 0 else ('none', '')
            nxt = toks[idx + 1] if idx + 1 < len(toks) else ('none', '')
            if glues(prev) and glues(nxt):
                toks[idx] = ('atom', v)
    return toks


ATOMK = {'atom', 'atomsym'}
SCRIPTK = {'sub', 'sup', 'star', 'sup2'}
FUNCWORDS = {'max': r'\max', 'min': r'\min'}


def bridge_latex(ch):
    return BRIDGEMAP.get(ch, ch)


def emit_run(run_toks):
    out = []
    subs, sups = [], []

    def flush_scripts():
        nonlocal subs, sups
        if subs:
            b = ''.join(subs)
            out.append('_' + (b if len(b) == 1 else '{' + b + '}'))
        if sups:
            b = ''.join(sups)
            out.append('^' + (b if len(b) == 1 else '{' + b + '}'))
        subs, sups = [], []

    for k, v in run_toks:
        if k == 'sub':
            subs.append(v)
        elif k == 'sup':
            sups.append(v)
        elif k == 'star':
            sups.append('*')
        elif k == 'sup2':
            sups.append('2')
        else:
            flush_scripts()
            if k in ATOMK:
                # space between adjacent Latin atoms: math mode ignores it,
                # and it keeps the word-fidelity tokenization letter-exact
                # (v2's Latin b would otherwise fuse into runs like "br")
                if (out and re.search(r'[A-Za-z]$', out[-1])
                        and re.match(r'[A-Za-z]', v)):
                    out.append(' ')
                out.append(v + ' ' if v.startswith('\\') and v[-1].isalpha() else v)
            elif k == 'bridge':
                out.append(bridge_latex(v))
            elif k == 'sp':
                out.append(' ')
            elif k == 'word':
                out.append(FUNCWORDS[v])
            else:
                raise AssertionError(f'bad token in run: {k}')
    flush_scripts()
    body = re.sub(r' {2,}', ' ', ''.join(out)).strip()
    return '$' + body + '$'


def assemble(toks):
    """Prose-mode token list -> list of ('text'|'math', str)."""
    n = len(toks)
    consumed = [False] * n
    runs = {}  # start index -> (list of tokens, end index)
    i = 0
    while i < n:
        if toks[i][0] not in ATOMK:
            i += 1
            continue
        start = end = i
        j = i + 1
        while j < n:
            k2, v2 = toks[j]
            if k2 in ATOMK or k2 in SCRIPTK:
                end = j
                j += 1
            elif k2 in ('bridge', 'sp') or (k2 == 'word' and v2 in FUNCWORDS):
                j += 1
            else:
                break
        # trailing: glued/spaced bridges after the last atom, minus separators;
        # opening brackets after the last atom belong to the following prose
        jj = end + 1
        while jj < n and toks[jj][0] in ('bridge', 'sp') and toks[jj][1] not in '([':
            jj += 1
        tail = list(range(end + 1, jj))
        # a run never ends in a separator or an opening bracket
        while tail and (toks[tail[-1]][0] == 'sp'
                        or (toks[tail[-1]][0] == 'bridge' and toks[tail[-1]][1] in ',.;:([')):
            tail.pop()
        idxs = list(range(start, end + 1)) + tail
        # leading: bridge chars before the first atom. Spaces are crossed only
        # toward an operator ("1 − a"), or toward digits once an operator has
        # been crossed; '.' joins only inside decimals. This keeps prose like
        # "Figure 4 (0.05 →" out of the run while capturing "(1 − a − λρ*)".
        p = start - 1
        lead = []
        crossed_op = False
        while p >= 0 and not consumed[p]:
            k2, v2 = toks[p]
            if k2 == 'sp':
                if p > 0 and not consumed[p - 1] and toks[p - 1][0] == 'bridge' and \
                        (toks[p - 1][1] in OPSET
                         or (crossed_op and toks[p - 1][1].isdigit())):
                    lead.insert(0, p)
                    p -= 1
                    continue
                break
            if k2 != 'bridge':
                break
            if v2 == '.' and not (p > 0 and toks[p - 1][0] == 'bridge'
                                  and toks[p - 1][1].isdigit()):
                break
            if v2 in OPSET:
                crossed_op = True
            lead.insert(0, p)
            p -= 1
        while lead and toks[lead[0]][0] == 'sp':
            lead.pop(0)
        idxs = lead + idxs

        # a run never starts with a closing bracket
        while idxs and toks[idxs[0]][0] == 'bridge' and toks[idxs[0]][1] in ')]':
            idxs.pop(0)
        while idxs and toks[idxs[0]][0] == 'sp':
            idxs.pop(0)

        def paren_bal(ix):
            s = ''.join(toks[t][1] for t in ix if toks[t][0] == 'bridge')
            return s.count('(') - s.count(')')

        while idxs and toks[idxs[0]] == ('bridge', '(') and paren_bal(idxs) > 0:
            idxs.pop(0)
        while idxs and toks[idxs[-1]] == ('bridge', ')') and paren_bal(idxs) < 0:
            idxs.pop()
        for t in idxs:
            consumed[t] = True
        runs[min(idxs)] = ([toks[t] for t in idxs], max(idxs))
        i = max(idxs) + 1

    res = []
    i = 0
    while i < n:
        if i in runs:
            run, mx = runs[i]
            res.append(('math', emit_run(run)))
            i = mx + 1
            continue
        k, v = toks[i]
        if k == 'sp':
            res.append(('text', ' '))
        elif k in ('word', 'bridge', 'other'):
            res.append(('text', v))
        elif k == 'star':
            res.append(('text', '*'))
        elif k in ATOMK:
            res.append(('math', '$' + v + '$'))
        elif k in SCRIPTK:
            raise AssertionError(f'orphan script token near {toks[max(0,i-3):i+3]}')
        else:
            raise AssertionError(k)
        i += 1
    return res


def render_inline(children, boldctx=False):
    segs = seglist(children, boldctx)
    pieces = []
    buf = []

    def flush():
        if not buf:
            return
        pieces.extend(assemble(flatten_tokens(buf)))
        buf.clear()

    for kind, val in segs:
        if kind in ('text', 'atom', 'sub', 'sup'):
            buf.append((kind, val))
        elif kind == 'textit':
            flush()
            # \emph, not \textit: toggles to upright inside italic theorem bodies
            pieces.append(('latex', r'\emph{' + esc_text(val) + '}'))
        elif kind == 'bold':
            flush()
            pieces.append(('latex', r'\textbf{' + render_inline(val, boldctx=True) + '}'))
        elif kind == 'tagspan':
            flush()
            pieces.append(('latex', r'{\footnotesize ' + render_inline(val) + '}'))
        elif kind == 'plainspan':
            flush()
            pieces.append(('latex', render_inline(val)))
        elif kind == 'br':
            flush()
            pieces.append(('latex', r'\\'))
        else:
            raise AssertionError(kind)
    flush()
    # merge adjacent text pieces so quote pairing sees full spans
    outp = []
    txt = []
    for kind, val in pieces:
        if kind == 'text':
            txt.append(val)
        else:
            if txt:
                outp.append(esc_text(''.join(txt)))
                txt = []
            outp.append(val)
    if txt:
        outp.append(esc_text(''.join(txt)))
    s = ''.join(outp)
    s = re.sub(r' {2,}', ' ', s).strip()
    for ph, latex in PLACEHOLDER_LATEX.items():
        s = s.replace(ph, latex)
    return s


# ---------------------------------------------------------------------------
# Cell 5 — display equations (everything is math; word phrases become \textit)

def render_eq(node):
    if 'exit floor' in text_of(node):
        return '\n'.join([
            r'\[',
            r'\begin{array}{c}',
            r'\textit{wage at task } x \;=\; s \;+\; [\,c\cdot\tilde{\rho}(x^*) - s\,]'
            r' \;+\; [\,\mu(x) - 1\,]\cdot c\cdot\tilde{\rho}(x^*)\\[3pt]',
            r'{\footnotesize \text{(exit floor)}\; + \;\text{(task premium)}\; + \;\text{(wedge rent)}}',
            r'\end{array}',
            r'\]'])
    toks = flatten_tokens(seglist(node['children']))
    # join hyphenated words, promote single-letter words to atoms
    merged = []
    for k, v in toks:
        if (k == 'other' and v == '-' and merged and merged[-1][0] == 'word'):
            merged[-1] = ('word', merged[-1][1] + '-')
        elif k == 'word' and merged and merged[-1][0] == 'word' and merged[-1][1].endswith('-'):
            merged[-1] = ('word', merged[-1][1] + v)
        else:
            merged.append((k, v))
    toks = [('atom', v) if (k == 'word' and len(v) == 1) else (k, v) for k, v in merged]

    out = []
    subs, sups = [], []

    def flush_scripts():
        nonlocal subs, sups
        if subs:
            b = ''.join(subs)
            out.append('_' + (b if len(b) == 1 else '{' + b + '}'))
        if sups:
            b = ''.join(sups)
            out.append('^' + (b if len(b) == 1 else '{' + b + '}'))
        subs, sups = [], []

    i, n = 0, len(toks)
    while i < n:
        k, v = toks[i]
        if k == 'sub':
            subs.append(v)
        elif k == 'sup':
            sups.append(v)
        elif k == 'star':
            sups.append('*')
        elif k == 'sup2':
            sups.append('2')
        else:
            flush_scripts()
            if k == 'word':
                if v in FUNCWORDS:
                    out.append(FUNCWORDS[v])
                else:
                    words = [v]
                    j = i + 1
                    while j + 1 <= n - 1 and toks[j][0] == 'sp' and toks[j + 1][0] == 'word' \
                            and toks[j + 1][1] not in FUNCWORDS and len(toks[j + 1][1]) > 1:
                        words.append(' ' + toks[j + 1][1])
                        j += 2
                    out.append(r'\textit{' + ''.join(words) + '}')
                    i = j - 1
            elif k in ATOMK:
                # same Latin-adjacency space as the prose emitter (fidelity)
                if (out and re.search(r'[A-Za-z]$', out[-1])
                        and re.match(r'[A-Za-z]', v)):
                    out.append(' ')
                out.append(v + ' ' if v.startswith('\\') and v[-1].isalpha() else v)
            elif k == 'sp':
                out.append(' ')
            elif k == 'bridge':
                out.append(bridge_latex(v))
            elif k == 'other':
                assert v in (EMSP, ':', ';'), f'unexpected char in eq: {v!r}'
                out.append(r'\quad ' if v == EMSP else v)
            else:
                raise AssertionError(f'unexpected token in eq: {k}')
        i += 1
    flush_scripts()
    body = ''.join(out).replace(r'\quad \quad ', r'\qquad ')
    body = re.sub(r' {2,}', ' ', body).strip()
    # orthodox style: number the mathematical displays; the schematic
    # word-chain displays (those carrying \textit phrases) stay unnumbered
    if r'\textit' in body:
        return '\\[\n' + body + '\n\\]'
    global _EQNUM_USED
    lab = EQNUM_LABELS[_EQNUM_USED]      # IndexError = a new display needs a label
    _EQNUM_USED += 1
    REFNUM[lab] = str(_EQNUM_USED)
    return '\\begin{equation}\\label{' + lab + '}\n' + body + '\n\\end{equation}'


# ---------------------------------------------------------------------------
# Cell 6 — block renderers

THEOREM_SEQ = []
EQ_COUNT = 0
FIG_EXPECT = ['fig_schedule.png', 'fig_eras.png', 'fig_deflator_fork.png',
              'fig_kappa.png', 'fig_fourway.png', 'fig_dyn_windfall.png',
              'fig_dyn_waterfall.png', 'fig_dyn_speedlag.png', 'fig_dyn_sloped.png']   # strata/ushape retired with Appendix B (2026-08-26)
TABLE_SPECS = [r'l p{8.6cm}', r'p{6.4cm} l p{4.6cm}',
               r'l p{9.6cm}']   # third: the Appendix F notation table

# ---- cross-reference label tables (stable under reordering) ----
HEAD_LABELS = {
    # main sections (h2 title after the number)
    'Introduction': 'sec:intro',
    'What standing accounts pin the wage to': 'sec:accounts',
    'The model: tasks and the margin': 'sec:model',
    'The ceiling: what prices the machine': 'sec:ceiling',
    'The floor: what prices exit': 'sec:floor',
    'The interval, closed': 'sec:interval',
    'The flat-capability limit: the real-wage fork': 'sec:limit',
    'The fiscal completion: rent tax and uniform dividend': 'sec:fiscal',
    'The fiscal completion: rent tax, uniform dividend, and the horizon': 'sec:fiscal',
    'History as three configurations of one schedule': 'sec:history',
    'History as three transitions of one schedule': 'sec:history',
    'Build time and the wage of waiting': 'sec:buildtime',
    'The model in motion: windfalls, waterfalls, and the buildout': 'sec:motion',
    'Implications for artificial intelligence': 'sec:ai',
    'Conclusion': 'sec:conclusion',
    'Measurement': 'sec:measurement',
    'Possible stabilizers': 'sec:stabilizers',
    'Stabilizers as quantity protections': 'sec:stabilizers',
    'Implications for artificial intelligence, and conclusion': 'sec:ai',
    # appendices
    'The environment and assignment equilibrium': 'app:environment',
    'Institutional wedges and directed adoption': 'app:wedges',
    'The machine sector in general form': 'app:machines',
    'The land-only closure': 'app:landonly',
    'CES consumption': 'app:ces',
    'The fiscal system in the sloped regime': 'app:fiscal',
    'Human-essential tasks': 'app:human',
    'Numerical methods and solver credibility': 'app:numerics',
    'The model in motion': 'app:motion',
    'The sequence economy': 'app:sequence-economy',
    'The steady-state equivalence': 'app:equivalence',
    'Notation': 'app:notation',
    'The open economy': 'app:open',
    'Prediction register': 'app:register',
    # subsections (h3 title after the number)
    'Marginal product': 'sec:marginal-product',
    'Search, matching, and bargaining': 'sec:search',
    'Task and assignment models': 'sec:tasks',
    'Institutional accounts': 'sec:institutions',
    'The classical accounts': 'sec:classical',
    'Automation and the wage': 'sec:automation',
    'Where the model meets data': 'sec:data',
    'Conditionality': 'app:conditionality',
    'Funding, and the incidence dial': 'app:funding',
    'Feasibility: the coverage ratio': 'app:coverage',
    'The race with enclosure': 'app:race',
    'The mix on the way down': 'app:mix',
    'Transition bases': 'app:transition-bases',
    'The sequence economy and the equivalence': 'sec:sequence',
    'The flat transition in closed form': 'sec:flat-closed',
    'The solver, validated before use': 'sec:solver-validated',
    'Windfall, waterfall, and speed times lag': 'sec:experiments',
    'The sloped path: which shock moves the wage': 'sec:sloped-path',
    'The steady-state pair': 'sec:fiscal-pair',
    'The fiscal horizon': 'sec:fiscal-horizon',
}
THEOREM_LABELS = {              # keyed on the number the HTML header declares
    # 2026-08-28 (later): dynamics to Appendix E; mains are 1-6 with the
    # interest identity demoted to prose; E.1/E.2 are the appendix results
    '1': 'prop:margin', '2': 'prop:replacement', '3': 'prop:exit',
    '4': 'prop:fork', '5': 'prop:welfare', '6': 'prop:horizon',
    'E.1': 'prop:equivalence', 'E.2': 'prop:frozen-rent',
    # 2026-08-26 restructure: landonly is now B, human-essential is now D
    # (wedges' lem:effective/prop:targeting retired with Appendix B's cut);
    # D.2/D.3 are the new fraud-bound and superstar lemmas.
    'A.1': 'lem:existence', 'B.1': 'prop:landonly',
    'D.1': 'prop:baumol', 'D.2': 'lem:fraud', 'D.3': 'lem:superstar',
}
FIG_LABELS = ['fig:schedule', 'fig:eras', 'fig:fork', 'fig:kappa',
              'fig:fourway', 'fig:dyn-windfall', 'fig:dyn-waterfall',
              'fig:dyn-speedlag', 'fig:dyn-sloped']   # parallel to FIG_EXPECT
EQNUM_LABELS = ['eq:gamma', 'eq:recursion', 'eq:build-price', 'eq:recursion-uK',
                'eq:closure', 'eq:lambda-zero', 'eq:user-cost',
                'eq:exit', 'eq:fork-price', 'eq:ces-share',
                'eq:net-rental']  # numbered displays, in order (E holds the last)
PRED_LABELS = ['pred:compression', 'pred:protection', 'pred:negative-sum',
               'pred:traps', 'pred:labor-share', 'pred:land-share',
               'pred:ai-sites', 'pred:fork', 'pred:scissors', 'pred:incidence',
               'pred:conditional', 'pred:hollow', 'pred:exit']

SEC_NUM2LABEL = {}   # '3'   -> label   (filled during the walk)
SUB_NUM2LABEL = {}   # '2.2' / 'F.4' -> label
APP_LET2LABEL = {}   # 'B'   -> label
REFNUM = {}          # label -> the number it prints (for the fidelity check)
_EQNUM_USED = 0


def head_label(title):
    lab = HEAD_LABELS.get(title)
    check(lab is not None, f'heading label defined for {title!r}')
    return lab or 'sec:UNLABELED'


def xref_text(s):
    """Rewrite literal cross-references into \\ref{...} against the maps
    built during the walk. KeyError (loud) on an unknown target."""
    def sec(num):
        return SUB_NUM2LABEL[num] if '.' in num else SEC_NUM2LABEL[num]

    def r(lab):
        return r'\ref{' + lab + '}'

    s = re.sub(r'\bSections (\d+)--(\d+)',
               lambda m: 'Sections~' + r(sec(m.group(1))) + '--' + r(sec(m.group(2))), s)
    s = re.sub(r'\bSections (\d+) and (\d+)\b',
               lambda m: 'Sections~' + r(sec(m.group(1))) + ' and ' + r(sec(m.group(2))), s)
    s = re.sub(r'\b([Ss]ection) (\d+(?:\.\d+)?)\b',
               lambda m: m.group(1) + '~' + r(sec(m.group(2))), s)
    s = re.sub(r'\bAppendices ([A-I]) and ([A-I])\b',
               lambda m: 'Appendices~' + r(APP_LET2LABEL[m.group(1)])
               + ' and ' + r(APP_LET2LABEL[m.group(2)]), s)
    s = re.sub(r'\bAppendix ([A-I]\.\d)\b',
               lambda m: 'Appendix~' + r(SUB_NUM2LABEL[m.group(1)]), s)
    s = re.sub(r'\bAppendix ([A-I])\b',
               lambda m: 'Appendix~' + r(APP_LET2LABEL[m.group(1)]), s)
    s = re.sub(r'\bPropositions (\d+) and (\d+)\b',
               lambda m: 'Propositions~' + r(THEOREM_LABELS[m.group(1)])
               + ' and ' + r(THEOREM_LABELS[m.group(2)]), s)
    s = re.sub(r'\bProposition ((?:[A-I]\.)?\d+)\b',
               lambda m: 'Proposition~' + r(THEOREM_LABELS[m.group(1)]), s)
    s = re.sub(r'\bLemma ([A-I]\.\d+)\b',
               lambda m: 'Lemma~' + r(THEOREM_LABELS[m.group(1)]), s)
    s = re.sub(r'\bFigure (\d+)\b',
               lambda m: 'Figure~' + r(FIG_LABELS[int(m.group(1)) - 1]), s)
    s = re.sub(r'\bPrediction (\d+)\b',
               lambda m: 'Prediction~' + r(PRED_LABELS[int(m.group(1)) - 1]), s)
    # bare "F.1" / "D.1" forms (subsection first, then theorem)
    s = re.sub(r'\b([A-I]\.\d)\b',
               lambda m: r(SUB_NUM2LABEL.get(m.group(1)) or THEOREM_LABELS[m.group(1)]), s)
    return s


HEADER_RE = re.compile(
    r'^(Proposition|Lemma|Corollary)\s*([0-9]+|[A-Z]\.[0-9]+)?\s*(?:\(([^)]*)\))?\.$')


def smart_join(items):
    """items: list of (kind, text). Blank line between blocks, except around
    displays that continue a sentence."""
    parts = []
    for idx, (kind, text) in enumerate(items):
        if idx:
            prev_kind = items[idx - 1][0]
            sep = '\n\n'
            if kind == 'eq' and prev_kind == 'p':
                sep = '\n'
            elif prev_kind == 'eq' and kind == 'p' and text[:1].islower():
                sep = '\n'
            parts.append(sep)
        parts.append(text)
    return ''.join(parts)


def render_proof(node):
    ch = node['children']
    first = ch[0]
    assert isinstance(first, dict) and first['tag'] == 'i' \
        and text_of(first).strip() == 'Proof.', 'proof must open with <i>Proof.</i>'
    body = render_inline(ch[1:])
    assert QED in body, 'proof must end with the QED mark'
    body = body.replace(QED, '').rstrip('~ ')
    return '\\begin{proof}\n' + body.strip() + '\n\\end{proof}'


def render_prop(node):
    global EQ_COUNT
    ch = [c for c in node['children'] if not (isinstance(c, str) and not c.strip())]
    first = ch[0]
    assert isinstance(first, dict) and first['tag'] == 'p'
    fch = first['children']
    head = fch[0]
    assert isinstance(head, dict) and head['tag'] == 'b'
    m = HEADER_RE.match(text_of(head).strip())
    assert m, f'unparsed theorem header: {text_of(head)!r}'
    envkind, number, name = m.group(1).lower(), m.group(2), m.group(3)
    THEOREM_SEQ.append((envkind, number))
    lab = THEOREM_LABELS.get(number)
    check(lab is not None, f'theorem label defined for {envkind} {number}')
    REFNUM[lab] = number
    opt = (f'[{esc_text(name)}]' if name else '') + '\\label{' + lab + '}'
    items = [('p', render_inline(fch[1:]))]
    for sub in ch[1:]:
        if isinstance(sub, dict) and sub['tag'] == 'p':
            items.append(('p', render_inline(sub['children'])))
        elif isinstance(sub, dict) and sub['tag'] == 'div' and cls(sub) == 'eq':
            EQ_COUNT += 1
            items.append(('eq', render_eq(sub)))
        else:
            raise AssertionError('unexpected node inside prop')
    return (f'\\begin{{{envkind}}}{opt}\n' + smart_join(items) + f'\n\\end{{{envkind}}}')


def render_corollary_p(node):
    ch = node['children']
    m = HEADER_RE.match(text_of(ch[0]).strip())
    assert m and m.group(1) == 'Corollary'
    THEOREM_SEQ.append(('corollary', None))
    return (f'\\begin{{corollary}}[{esc_text(m.group(3))}]\n'
            + render_inline(ch[1:]) + '\n\\end{corollary}')


def render_figure(node, fignum):
    img = find(node, 'img')
    cap = find(node, 'figcaption')
    src = img['attrs']['src'].split('/')[-1]
    check(src == FIG_EXPECT[fignum - 1], f'Figure {fignum} file is {src}')
    capch = cap['children']
    head = capch[0]
    assert isinstance(head, dict) and head['tag'] == 'b' \
        and text_of(head).strip() == f'Figure {fignum}.', f'caption head at figure {fignum}'
    lab = FIG_LABELS[fignum - 1]
    REFNUM[lab] = str(fignum)
    return '\n'.join([
        r'\begin{figure}[t!]', r'\centering',
        rf'\includegraphics[width=0.88\linewidth]{{figures/{src}}}',
        rf'\caption{{{render_inline(capch[1:])}}}',
        rf'\label{{{lab}}}',
        r'\end{figure}'])


def render_table(node, tindex):
    rows = [c for c in node['children'] if isinstance(c, dict) and c['tag'] == 'tr']
    lines = [r'\begin{center}', r'{\small',
             r'\begin{tabular}{' + TABLE_SPECS[tindex] + '}', r'\toprule']
    for ri, tr in enumerate(rows):
        cells = [c for c in tr['children'] if isinstance(c, dict) and c['tag'] in ('th', 'td')]
        lines.append(' & '.join(render_inline(c['children']) for c in cells) + r' \\')
        if ri == 0:
            lines.append(r'\midrule')
    lines += [r'\bottomrule', r'\end{tabular}', '}', r'\end{center}']
    return '\n'.join(lines)


def render_list(node):
    env = 'enumerate' if node['tag'] == 'ol' else 'itemize'
    items = [c for c in node['children'] if isinstance(c, dict) and c['tag'] == 'li']
    lines = [f'\\begin{{{env}}}']
    if env == 'enumerate':      # the prediction register: label every item
        check(len(items) == len(PRED_LABELS), f'register has {len(items)} items')
    for k, li in enumerate(items):
        lab = ''
        if env == 'enumerate':
            REFNUM[PRED_LABELS[k]] = str(k + 1)
            lab = '\\label{' + PRED_LABELS[k] + '} '
        lines.append(r'\item ' + lab + render_inline(li['children']))
    lines.append(f'\\end{{{env}}}')
    return '\n'.join(lines), len(items)


# ---------------------------------------------------------------------------
# Cell 7 — document shell

PREAMBLE = r'''% ============================================================
% Pinning the Wage to Scarcity and Technology
% Generated from paper/pinning.html by code/html_to_latex.py.
% The HTML stays canonical: edit there, re-run the converter.
% ============================================================
% Style: orthodox macro working paper (12pt, onehalf spacing, plain theorem
% style with italic statements, numbered equations, CM fonts).
\documentclass[12pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[a4paper, margin=2.5cm]{geometry}
\usepackage{setspace}
\onehalfspacing
\usepackage{amsmath, amssymb, amsthm}
\usepackage{bbm}
\usepackage{bm}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage[labelfont=bf, labelsep=period, font={footnotesize,stretch=1}, justification=justified]{caption}
\usepackage{microtype}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}

\theoremstyle{plain}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}[proposition]{Lemma}
\newtheorem*{corollary}{Corollary}

% hanging-indent entry for the hand-formatted reference list
\newcommand{\refentry}[1]{\par\hangindent=1.5em\hangafter=1\noindent #1}

\title{\bfseries Pinning the Wage to Scarcity and Technology\thanks{Views are the
  authors' own and do not represent those of KTH, SEB, or the Stockholm School of
  Economics. Written in collaboration with Claude (Anthropic); see the AI-use note
  at the end.
  % NOTE (generated): the HTML draftline reads "Views are the author's own and do
  % not represent those of KTH or SEB." — pluralized and extended to SSE when the
  % co-author was added. Reword as needed.
  }\\[7pt]
  \large\mdseries Replacement, exit, and the rents of non-produced inputs in a task economy}

% Author order: Wilson first (her call, 2026-08-21).
\author{Stella Wilson\thanks{KTH Royal Institute of Technology and Skandinaviska
    Enskilda Banken (SEB). Email: \texttt{thmwi@kth.se}.}
  \and
  Johan B\r{a}ge\thanks{Stockholm School of Economics.
    Email: \texttt{Johan.Bage@hhs.se}.
  }}

\date{Working draft --- August 2026}

\begin{document}
\maketitle
'''


# ---------------------------------------------------------------------------
# Cell 8 — main walk

def main():
    html_raw = SRC.read_text(encoding='utf-8')
    html = apply_specials(html_raw)
    root = parse(html)
    body = find(root, 'body')
    blocks = [c for c in body['children'] if isinstance(c, dict)]

    items = []          # (kind, text)
    section_no = 0
    subsection_no = 0
    fig_no = 0
    table_no = 0
    in_appendix = False
    appendix_letters = []
    pred_items = kill_items = ref_count = 0
    global EQ_COUNT

    for nd in blocks:
        tag, klass = nd['tag'], cls(nd)
        txt = text_of(nd).strip()

        if tag == 'h1' or (tag == 'div' and klass in ('subtitle', 'authorline', 'draftline')):
            continue
        if tag == 'div' and klass == 'abstract':
            head = nd['children'][0]
            assert isinstance(head, dict) and text_of(head).strip() == 'Abstract.'
            items.append(('abs', '\\begin{abstract}\n\\noindent '
                          + render_inline(nd['children'][1:]) + '\n\\end{abstract}\n'
                          '% TODO: JEL codes and keywords for the title page — suggestions,\n'
                          '% to be confirmed by the authors:\n'
                          '% \\noindent JEL: E25, J23, O33, H21. \\quad\n'
                          '% Keywords: automation, tasks, wages, land rents, outside option.'))
        elif tag == 'h2':
            m = re.match(r'^(\d+)\.\s+(.*)$', txt)
            ma = re.match(r'^Appendix ([A-I])\.\s+(.*)$', txt)
            if m:
                section_no += 1
                check(int(m.group(1)) == section_no, f'section {m.group(1)} in sequence')
                subsection_no = 0
                lab = head_label(m.group(2))
                SEC_NUM2LABEL[str(section_no)] = lab
                REFNUM[lab] = str(section_no)
                items.append(('sec', f'\\section{{{esc_text(m.group(2))}}}\\label{{{lab}}}'))
            elif ma:
                if not in_appendix:
                    in_appendix = True
                    items.append(('sec', '\\appendix\n'
                                  '\\counterwithin{proposition}{section}\n'
                                  '\\titleformat{\\section}{\\normalfont\\Large\\bfseries}'
                                  '{Appendix~\\thesection.}{0.6em}{}'))
                    section_no = 0
                section_no += 1
                appendix_letters.append(ma.group(1))
                check(ord(ma.group(1)) - 64 == section_no, f'appendix {ma.group(1)} in sequence')
                subsection_no = 0
                lab = head_label(ma.group(2))
                APP_LET2LABEL[ma.group(1)] = lab
                REFNUM[lab] = ma.group(1)
                items.append(('sec', f'\\section{{{esc_text(ma.group(2))}}}\\label{{{lab}}}'))
            elif txt == 'References':
                items.append(('sec', '\\section*{References}'))
            elif txt.startswith('Acknowledgements'):
                # per-author acknowledgements sections (split 2026-08-21);
                # Wilson's text is verbatim, Båge's section awaits his text
                items.append(('sec', f'\\section*{{{esc_text(txt)}}}'))
            else:
                raise AssertionError(f'unexpected h2: {txt!r}')
        elif tag == 'h3':
            m = re.match(r'^(\d+|[A-I])\.(\d+)\s+(.*)$', txt)
            assert m, f'unparsed h3: {txt!r}'
            subsection_no += 1
            check(int(m.group(2)) == subsection_no,
                  f'subsection {m.group(1)}.{m.group(2)} in sequence')
            lab = head_label(m.group(3))
            printed = f'{m.group(1)}.{subsection_no}'
            SUB_NUM2LABEL[printed] = lab
            REFNUM[lab] = printed
            items.append(('sec', f'\\subsection{{{esc_text(m.group(3))}}}\\label{{{lab}}}'))
        elif tag == 'p':
            first = nd['children'][0] if nd['children'] else None
            if klass == 'proof':
                items.append(('proof', render_proof(nd)))
            elif isinstance(first, dict) and first['tag'] == 'b' \
                    and text_of(first).strip().startswith('Corollary'):
                items.append(('prop', render_corollary_p(nd)))
            else:
                items.append(('p', render_inline(nd['children'])))
        elif tag == 'div' and klass == 'eq':
            EQ_COUNT += 1
            items.append(('eq', render_eq(nd)))
        elif tag == 'div' and klass == 'prop':
            items.append(('prop', render_prop(nd)))
        elif tag == 'figure':
            fig_no += 1
            items.append(('fig', render_figure(nd, fig_no)))
        elif tag == 'table':
            items.append(('table', render_table(nd, table_no)))
            table_no += 1
        elif tag in ('ol', 'ul'):
            rendered, count = render_list(nd)
            if tag == 'ol':
                pred_items = count
            else:
                kill_items = count
            items.append(('list', rendered))
        elif tag == 'div' and klass == 'refs':
            entries = [c for c in nd['children'] if isinstance(c, dict) and c['tag'] == 'p']
            ref_count = len(entries)
            body_lines = ['{\\small\\singlespacing'] + \
                ['\\refentry{' + render_inline(e['children']) + '}' for e in entries] + ['}']
            items.append(('refs', '\n'.join(body_lines)))
        elif tag == 'div' and klass == 'fnote':
            items.append(('fnote',
                          '\\bigskip\\par\\noindent\\rule{0.35\\linewidth}{0.4pt}\\par\\smallskip\n'
                          '\\noindent{\\footnotesize\\singlespacing '
                          + render_inline(nd['children']) + '\\par}'))
        else:
            raise AssertionError(f'unhandled block <{tag} class={klass!r}> {txt[:60]!r}')

    # cross-reference pass: rewrite literal mentions to \ref (references
    # list excluded -- author-year entries are literal by design)
    items = [(kind, text if kind == 'refs' else xref_text(text))
             for kind, text in items]
    leftover = [r'\b[Ss]ections? \d', r'\bAppendix [A-I]\b', r'\bAppendices [A-I]',
                r'\bPropositions? \d', r'\bProposition [A-I]\.', r'\bLemma [A-I]\.',
                r'\bFigures? \d', r'\bPredictions? \d', r'\b[A-I]\.\d\b']
    stray = sorted({pat for pat in leftover for kind, text in items
                    if kind != 'refs' and re.search(pat, text)})
    check(not stray, f'no literal cross-references survive the rewrite ({stray})')

    tex = PREAMBLE + '\n' + smart_join(items) + '\n\n\\end{document}\n'

    OUT.mkdir(exist_ok=True)
    (OUT / 'figures').mkdir(exist_ok=True)
    for f in FIG_EXPECT:
        shutil.copy2(FIGSRC / f, OUT / 'figures' / f)
    (OUT / 'main.tex').write_text(tex, encoding='utf-8')
    print(f'[info] wrote {OUT / "main.tex"} ({len(tex)} chars)')

    # ---------------- verification ----------------
    # appendix restructure 2026-08-26 (STATE log 26): A-I -> A-D. B cut to a
    # v2 dynamics 2026-08-28: E (numerical methods) and F (notation) added;
    # interest identity is Prop 3, equivalence 6, frozen rent 7, welfare 8,
    # horizon 9; the fork's corollary rides after Prop 5.
    check(in_appendix and section_no == 6, f'appendix count = {section_no}')
    check(appendix_letters == list('ABCDEF'), f'appendix letters {appendix_letters}')
    expected = [('proposition', '1'), ('proposition', '2'), ('proposition', '3'),
                ('proposition', '4'), ('corollary', None), ('proposition', '5'),
                ('proposition', '6'),
                ('lemma', 'A.1'), ('proposition', 'B.1'),
                ('proposition', 'D.1'), ('lemma', 'D.2'), ('lemma', 'D.3'),
                ('proposition', 'E.1'), ('proposition', 'E.2')]
    check(THEOREM_SEQ == expected, f'theorem sequence {THEOREM_SEQ}')
    check(fig_no == 9, f'figures: {fig_no}')
    check(EQ_COUNT == 14, f'display equations: {EQ_COUNT}')
    check(table_no == 3, f'tables: {table_no}')
    # the prediction register was cut in the 2026-08-26 restructure
    check(pred_items == 0, f'predictions: {pred_items}')
    # the S11 kill list was removed in Stella's 2026-08-21 voice pass
    check(kill_items == 0, f'kill-list items: {kill_items}')
    check(ref_count == 58, f'reference entries: {ref_count}')
    check(_EQNUM_USED == len(EQNUM_LABELS), f'equation labels used: {_EQNUM_USED}')
    refs_used = set(re.findall(r'\\ref\{([^}]*)\}', tex))
    labels_def = set(re.findall(r'\\label\{([^}]*)\}', tex))
    check(refs_used <= labels_def, f'undefined \\ref targets: {sorted(refs_used - labels_def)[:6]}')
    check(refs_used <= set(REFNUM), f'\\ref targets missing a print number: '
          f'{sorted(refs_used - set(REFNUM))[:6]}')

    begins = Counter(re.findall(r'\\begin\{(\w+\*?)\}', tex))
    ends = Counter(re.findall(r'\\end\{(\w+\*?)\}', tex))
    check(begins == ends, f'environment balance {begins - ends} / {ends - begins}')
    dollars = len(re.findall(r'(?<!\\)\$', tex))
    check(dollars % 2 == 0, f'unescaped $ count even ({dollars})')
    check(tex.count('{') == tex.count('}'), 'brace balance')
    bad = sorted({ch for ch in tex if ord(ch) > 127 and ch not in 'åé\u2014\u2013'})
    check(not bad, f'no stray non-ascii ({bad[:20]})')
    check('\u25a0' not in tex, 'all SPECIAL placeholders resolved')

    word_diff_check(html, tex)

    print()
    if FAIL:
        print(f'*** {len(FAIL)} CHECK(S) FAILED ***')
        sys.exit(1)
    print('ALL GREEN')


# ---------------------------------------------------------------------------
# Cell 9 — word-sequence fidelity check

DROP_TOKENS = {'max', 'min'}


def _tok(s):
    return [t.lower() for t in re.findall(r"[A-Za-z]{2,}|[0-9]+", s)
            if t.lower() not in DROP_TOKENS]


def html_words(html):
    root = parse(html)
    body = find(root, 'body')
    toks = []

    def norm(s):
        s = s.replace(SUP2, ' ')                      # sup/sub content is dropped on both sides
        s = re.sub(r'■PH\d+■', ' ', s)      # SPECIAL placeholders
        return ''.join(ch for ch in s if not unicodedata.combining(ch))

    def add(s):
        toks.extend(_tok(norm(s)))

    def walk(node, skip_first_bold=False):
        first = True
        for ch in node['children']:
            if isinstance(ch, str):
                add(ch)
                continue
            k = cls(ch)
            t = ch['tag']
            if t in ('img', 'br', 'sub', 'sup'):
                continue
            if t == 'h1' or (t == 'div' and k in ('subtitle', 'authorline', 'draftline')):
                continue
            if skip_first_bold and first and t == 'b':
                m = HEADER_RE.match(text_of(ch).strip())
                if m and m.group(3):
                    add(m.group(3))
                first = False
                continue
            first = False
            if t in ('h2', 'h3'):
                txt = text_of(ch).strip()
                txt = re.sub(r'^Appendix [A-I]\.\s+', '', txt)
                txt = re.sub(r'^(\d+|[A-I])\.(\d+)?\.?\s+', '', txt)
                add(txt)
                continue
            if t == 'p' and k == 'proof':
                walk({'tag': 'p', 'attrs': {}, 'children': ch['children'][1:]})
                continue
            if t == 'figcaption' or (t == 'div' and k == 'abstract'):
                walk(ch, skip_first_bold=True)
                continue
            if t == 'div' and k == 'prop':
                subs = [c for c in ch['children'] if isinstance(c, dict)]
                for j, sub in enumerate(subs):
                    walk(sub, skip_first_bold=(j == 0))
                continue
            if t == 'p' and text_of(ch).strip().startswith('Corollary ('):
                walk(ch, skip_first_bold=True)
                continue
            walk(ch)

    walk(body)
    return toks


def tex_words(tex):
    body = tex.split(r'\begin{abstract}', 1)[1]
    body = body.split(r'\end{document}')[0]
    body = re.sub(r'(?m)(?<!\\)%.*$', '', body)
    # cross-references: drop labels, resolve each \ref to the number it
    # prints so the word sequence still matches the HTML's literal numbers
    body = re.sub(r'\\label\{[^}]*\}', ' ', body)
    body = re.sub(r'~?\\ref\{([^}]*)\}', lambda m: ' ' + REFNUM[m.group(1)] + ' ', body)
    body = re.sub(r'(?m)^\\(appendix|counterwithin|titleformat|bigskip)\S*.*$', ' ', body)
    body = re.sub(r'(?m)^\\begin\{tabular\}.*$', ' ', body)
    body = re.sub(r'\\includegraphics\[[^\]]*\]\{[^}]*\}', ' ', body)
    body = re.sub(r'\\rule\{[^}]*\}\{[^}]*\}', ' ', body)
    body = re.sub(r'\\\\(\[[0-9.]+pt\])?', ' ', body)
    body = re.sub(r'\\mathrm\{[^}]*\}', ' ', body)    # subscript words (dropped both sides)
    body = body.replace(r'\mathbbm{1}', ' ')          # 𝟙 (dropped on the HTML side too)
    body = re.sub(r'[_^]\{[^{}]*\}', ' ', body)       # scripts are dropped on both sides
    body = re.sub(r'[_^][A-Za-z0-9*]', ' ', body)
    body = re.sub(r'\\begin\{\w+\*?\}(\[([^\]]*)\])?',
                  lambda m: ' ' + (m.group(2) or '') + ' ', body)
    body = re.sub(r'\\end\{\w+\*?\}', ' ', body)
    body = re.sub(r'\\[a-zA-Z]+', ' ', body)
    body = body.replace('~', ' ')
    return _tok(body)


def word_diff_check(html, tex):
    hw = html_words(html)
    tw = tex_words(tex)
    sm = difflib.SequenceMatcher(a=hw, b=tw, autojunk=False)
    diffs = [(op, hw[a0:a1][:8], tw[b0:b1][:8])
             for op, a0, a1, b0, b1 in sm.get_opcodes() if op != 'equal']
    print(f'[info] word tokens: html={len(hw)} tex={len(tw)}; diff hunks={len(diffs)}')
    for d in diffs[:40]:
        print('   diff:', d)
    check(len(diffs) == 0, 'word-sequence fidelity html vs tex')


if __name__ == '__main__':
    main()
