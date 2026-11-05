"""provenance_view.py — the rewrite in reading order, each paragraph marked by where it came from.

    python3 -B provenance_view.py MAIN.tex REWRITE.tex OUT.html "title"

Every paragraph of REWRITE is preceded by a LaTeX comment naming its source ("from main.tex L<n>,
verbatim", "from main.tex L<n>, edited: ...", "NEW (...)"). This view prints the paragraphs in order:
- verbatim paragraphs plain, with their main.tex line;
- edited paragraphs with a word diff against the cited main.tex lines (sentences of those lines that
  went elsewhere are trimmed from the ends of the diff);
- new paragraphs on a tinted background;
and ends with every sentence of MAIN's body that appears nowhere in REWRITE, by MAIN line.
LaTeX is lightly rendered; math stays as source.
"""
import difflib
import html
import re
import sys

MAIN, REW, OUT, TITLE = sys.argv[1:5]
main_lines = open(MAIN, encoding="utf-8").read().split("\n")
rew_lines = open(REW, encoding="utf-8").read().split("\n")


def strip_comments(s):
    return re.sub(r"(?<!\\)%.*", "", s)


def norm(s):
    s = strip_comments(s).replace("~", " ")
    return re.sub(r"\s+", " ", s).strip()


def light(s):
    """Light LaTeX rendering for reading; math left as source."""
    s = html.escape(s, quote=False)
    s = re.sub(r"\\textbf\{([^{}]*)\}", r"<b>\1</b>", s)
    s = re.sub(r"\\emph\{([^{}]*)\}", r"<i>\1</i>", s)
    s = re.sub(r"\\(?:sub)*section\*?\{([^{}]*)\}", r"<b class=h>\1</b>", s)
    s = re.sub(r"\\label\{[^{}]*\}", "", s)
    s = re.sub(r"\\(eq)?ref\{([^{}]*)\}", lambda m: f"<span class=ref>[{m.group(2)}]</span>", s)
    s = s.replace("---", "—").replace("--", "–").replace("``", "“").replace("''", "”")
    return s


# ---- paragraphs of REWRITE with their provenance comments
body_start = next(i for i, L in enumerate(rew_lines) if L.startswith("\\begin{document}")) + 1
blocks, pending, cur, start, prov = [], [], [], None, []
for i in range(body_start, len(rew_lines)):
    L = rew_lines[i]
    if re.match(r"^\s*%", L):
        if cur:
            blocks.append((prov, start, cur)); cur, start = [], None
        pending.append(L.strip().lstrip("%").strip())
        continue
    if not L.strip():
        if cur:
            blocks.append((prov, start, cur)); cur, start = [], None
        continue
    if pending:
        prov, pending = pending, []
    if start is None:
        start = i + 1
    cur.append(L)
if cur:
    blocks.append((prov, start, cur))


def classify(p, text):
    pl = p.lower()
    if re.match(r"^\s*\\(sub)*section", text) or text.strip().startswith("\\begin{figure") \
            or text.strip().startswith("\\begin{table"):
        kind = "struct"
    else:
        kind = None
    if pl.startswith("new"):
        return "new" if kind is None else kind
    if "from main.tex" in pl and ("edited" in pl or "restat" in pl or "then new" in pl):
        return "edited" if kind is None else kind
    if "from main.tex" in pl and "verbatim" in pl:
        return "verbatim" if kind is None else kind
    return "other" if kind is None else kind


def src_range(p):
    m = re.search(r"from main\.tex L(\d+)(?:\s*[-–]\s*L?(\d+))?", p)
    if not m:
        return None
    a = int(m.group(1)); b = int(m.group(2) or a)
    return a, b


def inline_diff(old, new):
    a, b = old.split(" "), new.split(" ")
    ops = difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes()
    # trim deletions at the ends: sentences of the cited lines that stand elsewhere
    while ops and ops[0][0] == "delete":
        ops = ops[1:]
    while ops and ops[-1][0] == "delete":
        ops = ops[:-1]
    out, nchg = [], 0
    for t, i1, i2, j1, j2 in ops:
        if t == "equal":
            out.append(light(" ".join(b[j1:j2])))
        else:
            nchg += 1
            if i2 > i1:
                out.append(f"<del>{light(' '.join(a[i1:i2]))}</del>")
            if j2 > j1:
                out.append(f"<ins>{light(' '.join(b[j1:j2]))}</ins>")
    return " ".join(out), nchg


counts = {"verbatim": 0, "edited": 0, "new": 0, "struct": 0, "other": 0}
words = {"verbatim": 0, "edited": 0, "new": 0, "struct": 0, "other": 0}
rows = []
for p, start, cur in blocks:
    ptxt = " ".join(p)
    text = "\n".join(cur)
    kind = classify(ptxt, text)
    nt = norm(text)
    counts[kind] += 1
    words[kind] += len(re.sub(r"\$[^$]*\$", "M", nt).split())
    rng = src_range(ptxt)
    tag = f"L{rng[0]}" + (f"–{rng[1]}" if rng and rng[1] != rng[0] else "") if rng else ""
    if kind == "edited" and rng:
        old = norm(" ".join(main_lines[rng[0] - 1:rng[1]]))
        body, nchg = inline_diff(old, nt)
    else:
        body = light(nt)
    label = {"verbatim": "yours, unchanged", "edited": "yours, edited", "new": "new",
             "struct": "heading / float", "other": ""}[kind]
    rows.append(
        f'<div class="p {kind}"><div class=tag><span class=k>{label}</span> {tag} '
        f'<span class=ln>rewrite line {start}</span></div><div class=t>{body}</div>'
        f'<details><summary>provenance note</summary><div class=prov>{html.escape(ptxt)}</div></details></div>'
    )

# ---- sentences of MAIN's body that appear nowhere in REWRITE
rew_norm = norm("\n".join(rew_lines))
mb = next(i for i, L in enumerate(main_lines) if L.startswith("\\begin{document}")) + 1
me = next((i for i, L in enumerate(main_lines) if "section*{References}" in L), len(main_lines))
section = ""
missing = []
for i in range(mb, me):
    L = main_lines[i]
    m = re.search(r"\\(?:sub)*section\*?\{([^{}]*)\}", L)
    if m:
        section = m.group(1)
    t = norm(L)
    if not t or t.startswith("\\begin") or t.startswith("\\end"):
        continue
    t2 = re.sub(r"\b(e\.g|i\.e|cf|et al|vs|U\.S)\.", lambda m: m.group(0).replace(".", "§"), t)
    for s in re.split(r"(?<=[.?!])\s+(?=[A-Z\\(`])", t2):
        s = s.replace("§", ".")
        if len(s.split()) < 5:
            continue
        if s not in rew_norm:
            missing.append((i + 1, section, s))

by_sec = {}
for ln, sec, s in missing:
    by_sec.setdefault(sec, []).append((ln, s))
miss_html = []
for sec, items in by_sec.items():
    lis = "".join(f"<li><span class=ln>L{ln}</span> {light(s)}</li>" for ln, s in items)
    openattr = "" if sec.startswith("Existing characterizations") else " open"
    miss_html.append(f"<details{openattr}><summary>{html.escape(sec)} — {len(items)} sentences</summary><ul>{lis}</ul></details>")

summary = (f"{counts['verbatim']} paragraphs yours unchanged ({words['verbatim']} words), "
           f"{counts['edited']} yours edited ({words['edited']} words), "
           f"{counts['new']} new ({words['new']} words), {counts['struct']} headings and floats. "
           f"{len(missing)} sentences of main.tex do not appear word for word in the rewrite (listed at the end, "
           f"by main.tex line). Each was cut, restated in a new result, or edited; an edited one also shows "
           f"above, in its paragraph's diff.")

css = """
:root{--bg:#fff;--fg:#1b1b1b;--muted:#6b6b6b;--new:#fff7d6;--newb:#e0c45c;--ed:#eef5ff;--edb:#7aa7e0;
--del:#b3261e;--delbg:#fde7e6;--ins:#1e6b2d;--insbg:#e3f5e6;--line:#e6e6e6}
@media (prefers-color-scheme: dark){:root{--bg:#161616;--fg:#e8e8e8;--muted:#9a9a9a;--new:#3a3317;--newb:#8a7428;
--ed:#17263a;--edb:#3f6ea8;--del:#ff8a80;--delbg:#3d1d1b;--ins:#8fdc9b;--insbg:#16331c;--line:#2c2c2c}}
body{background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif;max-width:860px;margin:0 auto;padding:16px}
h1{font-size:1.4em}.sum{color:var(--muted);margin-bottom:1.5em}
.p{border-left:4px solid var(--line);padding:6px 12px;margin:10px 0}
.p.new{background:var(--new);border-color:var(--newb)}.p.edited{background:var(--ed);border-color:var(--edb)}
.p.struct{border-color:transparent}.tag{font:12px/1.4 system-ui,sans-serif;color:var(--muted)}
.k{font-weight:600}.ln{color:var(--muted);font:12px system-ui,sans-serif}
del{color:var(--del);background:var(--delbg)}ins{color:var(--ins);background:var(--insbg);text-decoration:none}
.ref{color:var(--muted)}b.h{font-size:1.15em}details{font:13px/1.4 system-ui,sans-serif;color:var(--muted)}
.prov{white-space:pre-wrap;padding:4px 0}ul{padding-left:1.2em}li{margin:4px 0;font:15px/1.5 Georgia,serif;color:var(--fg)}
.legend span{display:inline-block;padding:1px 8px;margin-right:8px;border-left:4px solid}
"""
legend = ('<div class=legend><span style="border-color:var(--line)">yours, unchanged</span>'
          '<span style="background:var(--ed);border-color:var(--edb)">yours, edited (<del>removed</del> <ins>added</ins>)</span>'
          '<span style="background:var(--new);border-color:var(--newb)">new</span></div>')
doc = (f"<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
       f"<title>{html.escape(TITLE)}</title><style>{css}</style><h1>{html.escape(TITLE)}</h1>"
       f"<div class=sum>{html.escape(summary)}</div>{legend}{''.join(rows)}"
       f"<h1>Sentences of main.tex not word for word in the rewrite</h1>{''.join(miss_html)}")
open(OUT, "w", encoding="utf-8").write(doc)
print(summary)
